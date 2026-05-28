import json
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.youtube import extract_video_id, get_video_transcript
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
                    'video_id': video_id,
                    'title': existing_material.title
                }, status=200)
                
            # 1. Fetch transcript
            transcript = get_video_transcript(video_id)
            
            # 2. Generate materials using AI
            materials = generate_study_materials(transcript)
            
            # 3. Save to database
            StudyMaterial.objects.create(
                user=request.user,
                video_id=video_id,
                title=f"Video Notes ({video_id})",
                notes=materials.get('notes', ''),
                summary=materials.get('summary', ''),
                quiz=materials.get('quiz', [])
            )
            
            # 4. Include video ID for embedding
            materials['video_id'] = video_id
            
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

