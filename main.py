from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv
import os
import google.generativeai as genai

from chat import render_page

load_dotenv()

app = FastAPI(title="ChatBot")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")

# In-memory chat history (Python replacement for client-side chat.js state)
messages: list[dict] = []


@app.get("/", response_class=HTMLResponse)
async def index():
    return render_page(messages)


@app.post("/chat", response_class=HTMLResponse)
async def chat(message: str = Form(...)):
    user_text = message.strip()
    if not user_text:
        return RedirectResponse("/", status_code=303)

    messages.append({"role": "user", "text": user_text})
    print(user_text,"user_text----->")
    response = model.generate_content(user_text)
    bot_text = response.text or ""
    messages.append({"role": "bot", "text": bot_text})
    print(bot_text,"bot_text----->")
    return RedirectResponse("/", status_code=303)


@app.post("/clear")
async def clear():
    messages.clear()
    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
