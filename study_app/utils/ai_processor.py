import os
import json
from groq import Groq

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def generate_study_materials(transcript_text):
    """
    Sends the transcript to the Groq API and requests a JSON response
    containing notes, summary, and a quiz.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    client = Groq(api_key=api_key)

    system_prompt = """
    You are an expert educational AI assistant.
    The user will provide the transcript of a YouTube video or the text of an article. 
    The text might be in Hindi or another language, but YOU MUST TRANSLATE and generate your entire output strictly in ENGLISH.
    You must output a JSON object containing the following keys:
    1. "notes": Detailed, section-by-section bullet points capturing all key concepts in English. Format as a string of HTML bullet points or Markdown. If timestamps (e.g. [01:23]) are present in the text, preserve them in your notes at relevant points so the user knows when the topic was discussed.
    2. "summary": A concise 2-3 paragraph overview of the video content in English.
    3. "quiz": An array of 5 Multiple Choice Questions (MCQs) in English based strictly on the content. Each question should be an object with "question", "options" (array of 4 strings), and "answer" (the correct string from options).
    4. "flashcards": An array of 5 to 10 flashcards in English. Each flashcard should be an object with "front" (the term/concept) and "back" (the definition/explanation).
    5. "mindmap": A Mermaid JS graph strictly in Mermaid syntax representing a mind map of the core concepts in the text (use flowchart or mindmap syntax). Do not wrap in markdown tags like ```mermaid.
    
    Ensure your response is ONLY a valid JSON object, with no markdown code block wrapping or additional text.
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Transcript:\n\n{transcript_text}"}
            ],
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        response_content = completion.choices[0].message.content
        return json.loads(response_content)
    except Exception as e:
        raise Exception(f"Failed to generate AI materials: {str(e)}")
