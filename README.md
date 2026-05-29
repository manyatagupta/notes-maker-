# Notes Maker AI

Notes Maker AI is a web application that takes any YouTube video or Article URL and instantly generates comprehensive study materials using Artificial Intelligence.

## Features

1. **Detailed Notes:** Section-by-section bullet points capturing all key concepts, complete with clickable timestamps.
2. **Summary:** A concise 2-3 paragraph overview of the content.
3. **Flashcards:** Auto-generated interactive flashcards for spaced repetition.
4. **Quiz Generation:** Multiple Choice Questions (MCQs) to test your knowledge with immediate feedback.
5. **PDF & Word Export:** Download your generated materials for offline studying.
6. **Dark Mode:** A sleek dark mode UI for late-night study sessions.
7. **Shareable Links:** Generate a unique link to share your study materials with others.
8. **Article Support:** In addition to YouTube videos, you can paste article URLs to generate materials from text.

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, TailwindCSS, Vanilla JS
- **AI Integration:** Groq API (LLaMA3/Mixtral)
- **Other Utilities:** 
  - `youtube-transcript-api` (for fetching transcripts)
  - `beautifulsoup4` (for scraping articles)
  - `html2pdf.js` (for PDF exports)
  - `python-docx` (for Word exports)

## Setup

1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment.
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
6. Run migrations: `python manage.py migrate`
7. Start the server: `python manage.py runserver`

## Usage

1. Register for an account or log in.
2. Paste a YouTube URL or an Article URL into the input field.
3. Wait for the AI to generate your study materials.
4. Use the tabs to navigate between Notes, Summary, Flashcards, and Quiz.
5. Export or share your materials using the provided buttons!
