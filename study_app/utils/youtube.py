import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def extract_video_id(url):
    """
    Extracts the video ID from various forms of YouTube URLs.
    """
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_video_transcript(video_id):
    """
    Fetches the transcript for the given YouTube video ID.
    Returns the transcript as a single string or raises an Exception.
    """
    try:
        # Fetch the transcript list
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        # Try to find an English transcript first
        try:
            transcript = transcript_list.find_transcript(['en'])
        except:
            # If English is not available, grab the first available transcript
            try:
                # get the first available transcript
                transcript = next(iter(transcript_list))
            except StopIteration:
                raise Exception("No transcripts available for this video.")
                
        # Fetch the actual transcript data (in its original language)
        # We rely on the LLM (Groq) to translate it to English during processing.
        transcript_data = transcript.fetch()
        
        # Format the transcript into a plain text string
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript_data)
        
        return text_formatted
    except Exception as e:
        error_msg = str(e)
        if "no element found" in error_msg.lower() or "too many requests" in error_msg.lower():
            raise Exception("YouTube has temporarily blocked transcripts for this video (or your network is rate-limited). Please try a different video.")
        else:
            raise Exception(f"Failed to fetch transcript: {error_msg}")
