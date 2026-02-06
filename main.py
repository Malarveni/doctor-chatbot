import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from groq import Groq

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# Initialize Groq client
# --------------------------------------------------
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing. Check your .env file.")

client = Groq(api_key=api_key)


# --------------------------------------------------
# FastAPI app
# --------------------------------------------------
app = FastAPI(
    title="Doctor Assistant Chatbot API",
    description="AI-powered medical assistant for doctors",
    version="1.0.0"
)

# --------------------------------------------------
# Enable CORS
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Serve static frontend files (CSS, JS)
# --------------------------------------------------
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# --------------------------------------------------
# Request & Response Models
# --------------------------------------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# --------------------------------------------------
# System Prompt
# --------------------------------------------------
SYSTEM_PROMPT = """
You are an AI Doctor Assistant.
You help doctors with:
- Medical explanations
- Differential diagnoses
- Treatment guidelines
- Drug information
- Clinical reasoning

Rules:
- Do NOT provide definitive diagnoses
- Do NOT replace professional medical judgment
- Keep responses concise, clinical, and evidence-based
- If unsure, say so clearly
"""

# --------------------------------------------------
# Chat API
# --------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
def chat_with_doctor_assistant(request: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            temperature=0.3,
            max_tokens=500
        )

        return ChatResponse(
            reply=completion.choices[0].message.content
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------------------------------
# Homepage Route (SERVES FRONTEND)
# --------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()
