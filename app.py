from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

# 1. INITIALIZE APP ONCE
app = FastAPI()

# 2. ADD MIDDLEWARE ONCE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. INITIALIZE CLIENT
# Note: I used the key from your previous message, but it's safer to use Render Env Vars
api_key = os.environ.get("GROQ_API_KEY", "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")
client = Groq(api_key=api_key)

# 4. DATA MODELS
class ResumeRequest(BaseModel):
    name: str
    email: str
    skills: str
    experience: str
    education: str

class QueryData(BaseModel):
    question: str

# 5. RESUME ROUTE
@app.post("/generate-resume")
async def generate_resume(request: ResumeRequest):
    prompt = f"Create a professional engineering resume for: {request.name}. Skills: {request.skills}."
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": prompt}]
        )
        # Ensure key is 'resume' to match your JS result.resume
        return {"resume": completion.choices[0].message.content}
    except Exception as e:
        print(f"RESUME ERROR: {e}")
        return {"error": str(e)}

# 6. QUERY ROUTE
@app.post("/query")
async def ask_question(data: QueryData):
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": data.question}],
            model="llama-3.1-8b-instant",
        )
        return {"answer": completion.choices[0].message.content}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
