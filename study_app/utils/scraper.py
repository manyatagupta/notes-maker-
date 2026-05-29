import requests
from bs4 import BeautifulSoup
import re

def is_youtube_url(url):
    pattern = r'(?:youtube\.com|youtu\.be)'
    return bool(re.search(pattern, url))

def get_article_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.extract()
            
        text = soup.get_text(separator=' ')
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limit text to ~20000 characters to avoid huge payloads
        return text[:20000]
    except Exception as e:
        raise Exception(f"Failed to extract article text: {str(e)}")
