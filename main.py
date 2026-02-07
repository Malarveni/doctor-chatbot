import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
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
    # This print helps debug logs in Render if it fails
    print("Error: GROQ_API_KEY not found.") 

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
# Chat API Route
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
        print(f"Error: {e}") # Print error to logs
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------------------------------
# Serve Frontend Files (Updated for Flat Structure)
# --------------------------------------------------

# Serve the HTML at the root URL
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return FileResponse("index.html")

# Serve the CSS file
@app.get("/style.css")
async def serve_css():
    return FileResponse("style.css")

# Serve the JS file
@app.get("/app.js")
async def serve_js():
    return FileResponse("app.js")
