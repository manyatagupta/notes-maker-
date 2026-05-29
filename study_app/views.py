import json
import io
from docx import Document
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.youtube import extract_video_id, get_video_transcript
from .utils.scraper import is_youtube_url, get_article_text
from .utils.ai_processor import generate_study_materials

def index(request):
    """
    Renders the main frontend page.
    """
    return render(request, 'study_app/index.html')

@csrf_exempt
@login_required
def generate_materials(request):
    """
    API endpoint that receives a YouTube URL and returns the generated
    study materials (Notes, Summary, Quiz) in JSON format.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url', '')
            
            if not url:
                return JsonResponse({'error': 'No URL provided.'}, status=400)
            
            is_yt = is_youtube_url(url)
            video_id = ""
            
            if is_yt:
                video_id = extract_video_id(url)
                if not video_id:
                    return JsonResponse({'error': 'Invalid YouTube URL.'}, status=400)
                    
                # Check if this user has already generated materials for this video
                from .models import StudyMaterial
                existing_material = StudyMaterial.objects.filter(user=request.user, video_id=video_id).first()
                if existing_material:
                    return JsonResponse({
                        'notes': existing_material.notes,
                        'summary': existing_material.summary,
                        'quiz': existing_material.quiz,
                        'flashcards': existing_material.flashcards,
                        'video_id': video_id,
                        'title': existing_material.title,
                        'material_id': existing_material.id
                    }, status=200)
                    
                # 1. Fetch transcript
                content_text = get_video_transcript(video_id)
                title = f"Video Notes ({video_id})"
            else:
                # Treat as article
                content_text = get_article_text(url)
                title = f"Article Notes"
            
            # 2. Generate materials using AI
            materials = generate_study_materials(content_text)
            
            # 3. Save to database
            new_material = StudyMaterial.objects.create(
                user=request.user,
                video_id=video_id, # Can be empty for articles
                title=title,
                notes=materials.get('notes', ''),
                summary=materials.get('summary', ''),
                quiz=materials.get('quiz', []),
                flashcards=materials.get('flashcards', [])
            )
            materials['material_id'] = new_material.id
            
            # 4. Include video ID for embedding
            if is_yt:
                materials['video_id'] = video_id
            else:
                materials['video_id'] = None
            
            return JsonResponse(materials, status=200)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def register(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'study_app/register.html', {'form': form})

@login_required
def dashboard(request):
    """
    Shows a history of all generated study materials for the logged-in user.
    """
    from .models import StudyMaterial
    materials = StudyMaterial.objects.filter(user=request.user)
    return render(request, 'study_app/dashboard.html', {'materials': materials})

@login_required
def export_word(request, material_id):
    from .models import StudyMaterial
    material = get_object_or_404(StudyMaterial, id=material_id, user=request.user)
    
    document = Document()
    document.add_heading(material.title, 0)
    
    document.add_heading('Summary', level=1)
    document.add_paragraph(material.summary)
    
    document.add_heading('Notes', level=1)
    # Basic HTML strip for notes (can be improved)
    import re
    notes_text = re.sub('<[^<]+>', '', material.notes)
    document.add_paragraph(notes_text)
    
    document.add_heading('Quiz', level=1)
    for i, q in enumerate(material.quiz):
        document.add_paragraph(f"Q{i+1}: {q.get('question')}")
        for opt in q.get('options', []):
            document.add_paragraph(f"- {opt}")
        document.add_paragraph(f"Answer: {q.get('answer')}\n")
    
    f = io.BytesIO()
    document.save(f)
    f.seek(0)
    
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="StudyMaterial_{material_id}.docx"'
    return response

