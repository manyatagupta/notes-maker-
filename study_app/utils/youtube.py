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
        # First attempt: youtube_transcript_api
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        try:
            transcript = transcript_list.find_transcript(['en'])
        except:
            try:
                transcript = next(iter(transcript_list))
            except StopIteration:
                raise Exception("No transcripts available for this video.")
                
        transcript_data = transcript.fetch()
        
        formatted_lines = []
        for entry in transcript_data:
            start_time = int(getattr(entry, 'start', 0) if not isinstance(entry, dict) else entry.get('start', 0))
            minutes = start_time // 60
            seconds = start_time % 60
            time_str = f"[{minutes:02d}:{seconds:02d}]"
            text = (getattr(entry, 'text', '') if not isinstance(entry, dict) else entry.get('text', '')).replace('\n', ' ')
            formatted_lines.append(f"{time_str} {text}")
            
        return "\n".join(formatted_lines)
        
    except Exception as e:
        error_msg = str(e).lower()
        if "too many requests" in error_msg or "no element found" in error_msg or "ipblocked" in error_msg or "could not retrieve a transcript" in error_msg:
            # Fallback to yt-dlp
            try:
                import yt_dlp
                import requests
                
                ydl_opts = {
                    'writesubtitles': True, 
                    'writeautomaticsub': True, 
                    'subtitleslangs': ['en'], 
                    'skip_download': True, 
                    'quiet': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
                    subs = info.get('subtitles', {}) or info.get('automatic_captions', {})
                    en_subs = subs.get('en', [])
                    
                    if not en_subs:
                        raise Exception("No subtitles found via yt-dlp either.")
                        
                    # Find json3 format (which has timestamps)
                    json_url = next((s['url'] for s in en_subs if s['ext'] == 'json3'), None)
                    if not json_url:
                        raise Exception("No json3 subtitle format available.")
                        
                    resp = requests.get(json_url, timeout=10)
                    resp.raise_for_status()
                    sub_data = resp.json()
                    
                    formatted_lines = []
                    events = sub_data.get('events', [])
                    for event in events:
                        start_ms = event.get('tStartMs', 0)
                        start_time = start_ms // 1000
                        minutes = start_time // 60
                        seconds = start_time % 60
                        time_str = f"[{minutes:02d}:{seconds:02d}]"
                        
                        # Extract text
                        segs = event.get('segs', [])
                        if not segs:
                            continue
                        text = "".join(seg.get('utf8', '') for seg in segs).replace('\n', ' ').strip()
                        if text:
                            formatted_lines.append(f"{time_str} {text}")
                            
                    if not formatted_lines:
                        raise Exception("Extracted subtitles were empty.")
                        
                    return "\n".join(formatted_lines)
            except Exception as yt_e:
                raise Exception(f"YouTube has temporarily blocked transcripts for this video (or your network is rate-limited). Fallback also failed: {str(yt_e)}")
        else:
            raise Exception(f"Failed to fetch transcript: {str(e)}")
