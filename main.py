from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv
import os
import google.generativeai as genai

from validators import SignupData, format_validation_error
from chat import render_page
from createUser import render_create_user_page
from login import render_login_page
from firestore_client import (
    insert_user_full,
    get_user_by_email,
    get_user_by_id,
    insert_chat_session,
    insert_message,
    verify_password,
)
from pydantic import ValidationError

load_dotenv()

app = FastAPI(title="ChatBot")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-flash-latest")

user_messages: dict[str, list[dict]] = {}
user_sessions: dict[str, str] = {}


def get_logged_in_user_id(request: Request) -> str | None:
    return request.cookies.get("user_id")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return RedirectResponse("/login", status_code=303)

    user = get_user_by_id(user_id)
    if not user:
        # cookie points to a user that no longer exists in Firestore
        response = RedirectResponse("/login", status_code=303)
        response.delete_cookie("user_id")
        return response

    messages = user_messages.setdefault(user_id, [])
    return render_page(messages, username=user.get("firstName", "there"))


@app.get("/signup", response_class=HTMLResponse)
async def signup_page():
    return render_create_user_page()

@app.post("/signup")
async def signup(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(""),
    age: str = Form(""),
    country: str = Form(""),
):
    try:
        data = SignupData(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone=phone,
            age=age or 0,
            country=country,
        )
    except ValidationError as e:
        return HTMLResponse(render_create_user_page(error=format_validation_error(e)))

    existing = get_user_by_email(data.email)
    if existing:
        return HTMLResponse(render_create_user_page(error="An account with this email already exists."))

    user_id = insert_user_full(
        data.first_name, data.last_name, data.email, data.password, data.phone, data.age, data.country
    )

    session_id = insert_chat_session(user_id=user_id, topic="General Chat")
    user_sessions[user_id] = session_id
    user_messages[user_id] = []

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(key="user_id", value=user_id, httponly=True)
    return response

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return render_login_page()


@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email)
    if not user or not verify_password(password, user.get("passwordHash", "")):
        return HTMLResponse(render_login_page(error="Invalid email or password."))

    user_id = user["id"]
    if user_id not in user_sessions:
        session_id = insert_chat_session(user_id=user_id, topic="General Chat")
        user_sessions[user_id] = session_id
        user_messages[user_id] = []

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(key="user_id", value=user_id, httponly=True)
    return response


@app.post("/logout")
async def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("user_id")
    return response


@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return RedirectResponse("/login", status_code=303)

    user_text = message.strip()
    if not user_text:
        return RedirectResponse("/", status_code=303)

    session_id = user_sessions[user_id]
    messages = user_messages.setdefault(user_id, [])

    messages.append({"role": "user", "text": user_text})
    insert_message(session_id, "user", user_text)

    response_text = model.generate_content(user_text)
    bot_text = response_text.text or ""
    messages.append({"role": "bot", "text": bot_text})
    insert_message(session_id, "bot", bot_text)

    return RedirectResponse("/", status_code=303)


@app.post("/clear")
async def clear(request: Request):
    user_id = get_logged_in_user_id(request)
    if user_id and user_id in user_messages:
        user_messages[user_id].clear()
    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)