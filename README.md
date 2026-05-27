# Notes Maker AI

A Django-based web application that automatically generates comprehensive study materials (detailed notes, summaries, and MCQs) from YouTube videos using Groq's Llama 3 models.

## Features
- **YouTube Transcript Extraction:** Automatically pulls transcripts from any public YouTube video.
- **AI Processing:** Uses LLaMA-3 (via Groq API) to generate Notes, Summary, and a 5-question Quiz.
- **Authentication System:** Secure user registration and login functionality.
- **Responsive UI:** Built with Tailwind CSS for a clean, modern, and mobile-friendly interface.

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/manyatagupta/notes-maker-.git
   cd notes-maker-
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On MacOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   - Copy `.env.example` to `.env`
   - Fill in your `GROQ_API_KEY` and `YOUTUBE_API_KEY` in `.env`.

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` in your browser.
