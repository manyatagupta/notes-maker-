import os
import json
from groq import Groq

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def generate_study_materials(transcript_text, difficulty="standard"):
    """
    Sends the transcript to the Groq API and requests a JSON response
    containing notes, summary, and a quiz.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    client = Groq(api_key=api_key)
    
    difficulty_prompt = ""
    if difficulty == "simple":
        difficulty_prompt = "\nThe user has requested the output to be extremely simplified (Explain Like I'm 5 style). Use fun analogies and very simple words."
    elif difficulty == "advanced":
        difficulty_prompt = "\nThe user has requested an advanced, highly technical output suitable for university-level understanding. Go deep into nuances."

    system_prompt = f"""
    You are an expert educational AI assistant.{difficulty_prompt}
    The user will provide the transcript of a YouTube video or the text of an article. 
    The text might be in Hindi or another language, but YOU MUST TRANSLATE and generate your entire output strictly in ENGLISH.
    You must output a JSON object containing the following keys:
    1. "notes": Detailed, section-by-section bullet points capturing all key concepts in English. Format as a string of HTML bullet points or Markdown. If timestamps (e.g. [01:23]) are present in the text, preserve them in your notes at relevant points so the user knows when the topic was discussed.
    2. "summary": A highly detailed and comprehensive summary of the video content in English, spanning at least 4 to 6 paragraphs. It should cover all main arguments, facts, key examples, and conclusions discussed.
    3. "quiz": An array of 5 Multiple Choice Questions (MCQs) in English based strictly on the content. Each question should be an object with "question", "options" (array of 4 strings), and "answer" (the correct string from options).
    4. "flashcards": An array of 5 to 10 flashcards in English. Each flashcard should be an object with "front" (the term/concept) and "back" (the definition/explanation).
    5. "mindmap": A Mermaid JS graph strictly in Mermaid syntax representing a mind map of the core concepts in the text (use flowchart or mindmap syntax). Do not wrap in markdown tags like ```mermaid.
    
    Ensure your response is ONLY a valid JSON object, with no markdown code block wrapping or additional text.
    """

    try:
        # Truncate to ~3,000 chars to avoid exceeding 6,000 TPM Groq free tier limit (especially for non-English texts which consume more tokens)
        max_chars = 3000
        if len(transcript_text) > max_chars:
            transcript_text = transcript_text[:max_chars] + "\n\n[... Transcript truncated due to API length limits ...]"

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Transcript:\n\n{transcript_text}"}
            ],
            temperature=0.5,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        response_content = completion.choices[0].message.content
        return json.loads(response_content)
    except Exception as e:
        raise Exception(f"Failed to generate AI materials: {str(e)}")

def chat_with_document(document_text, user_question, history=None):
    """
    Sends the document text, chat history, and user's question to Groq API.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    client = Groq(api_key=api_key)
    system_prompt = (
        "You are a friendly, encouraging, and highly intelligent AI tutor. "
        "Your goal is to help the user learn and understand the provided document text. "
        "Engage in a natural conversation. If they say hi, greet them enthusiastically. "
        "Answer their questions based on the document. If an answer isn't in the document, "
        "you can use your general knowledge, but clarify that it's outside the provided text. "
        "Use markdown formatting to make your responses beautiful and readable."
    )
    
    try:
        max_chars = 3000
        if len(document_text) > max_chars:
            document_text = document_text[:max_chars] + "\n\n[... Text truncated ...]"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Context Document:\n\n{document_text}"}
        ]
        
        if history and isinstance(history, list):
            for msg in history:
                if msg.get("role") in ["user", "assistant"] and msg.get("content"):
                    messages.append({"role": msg["role"], "content": msg["content"]})
                    
        messages.append({"role": "user", "content": user_question})

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def translate_document(document_text, target_language):
    """
    Translates the document text into the specified target language using Groq API.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    client = Groq(api_key=api_key)
    system_prompt = f"You are an expert translator. Translate the following study materials into {target_language}. Maintain the original formatting, including bullet points, bold text, and timestamps. Do not add any extra commentary."
    try:
        max_chars = 3000
        if len(document_text) > max_chars:
            document_text = document_text[:max_chars] + "\n\n[... Text truncated ...]"

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Text to translate:\n\n{document_text}"}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error translating text: {str(e)}"

def eli5_document(document_text):
    """
    Simplifies the document text to an 'Explain Like I'm 5' (ELI5) level using Groq API.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    client = Groq(api_key=api_key)
    system_prompt = "You are an expert teacher who specializes in making complex topics extremely simple. Rewrite the following text so that a 5-year-old could easily understand it. Use fun analogies and very simple words. Maintain bullet points if they exist."
    try:
        max_chars = 3000
        if len(document_text) > max_chars:
            document_text = document_text[:max_chars] + "\n\n[... Text truncated ...]"

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Text to simplify:\n\n{document_text}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating ELI5 text: {str(e)}"
