# Simple ChatBot (FastAPI)

Simple chatbot for learning and implementing APIs in FastAPI with Google Gemini.
All logic is in Python — no Jinja2, no JavaScript.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Add your Gemini API key in `.env`:

```
GEMINI_API_KEY="your_gemini_api_key_here"
```

3. Run the app:

```bash
python app.py
```

Or:

```bash
uvicorn app:app --reload
```

4. Open http://127.0.0.1:8000
