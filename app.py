from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ MOST COMPATIBLE MODEL
model = genai.GenerativeModel("models/gemini-flash-latest")
# model = genai.GenerativeModel("models/gemini-1.0-pro")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    response = model.generate_content(user_message)

    return jsonify({
        "reply": response.text
    })

if __name__ == "__main__":
    app.run(debug=True)