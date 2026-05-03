from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

# 1. Initialize App ONCE
app = FastAPI()

# 2. Add Middleware ONCE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Initialize Client (Using Environment Variable is safer)
# On Render, make sure you added GROQ_API_KEY in Environment Variables
api_key = os.environ.get("GROQ_API_KEY", "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")
client = Groq(api_key=api_key)

# 4. Data Models
class ResumeRequest(BaseModel):
    name: str
    email: str
    skills: str
    experience: str
    education: str

class QueryData(BaseModel):
    question: str

# 5. RESUME ROUTE (Ends in /generate-resume)
@app.post("/generate-resume")
async def generate_resume(request: ResumeRequest):
    prompt = f"""
    You are an expert resume builder. Create a professional, clean resume for:
    NAME: {request.name}
    EMAIL: {request.email}
    SKILLS: {request.skills}
    EXPERIENCE: {request.experience}
    EDUCATION: {request.education}
    
    Format the output clearly using Markdown. Use bold headers and bullet points.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": prompt}]
        )
        # Match your JavaScript result.resume
        return {"resume": completion.choices[0].message.content}
    except Exception as e:
        print(f"RESUME ERROR: {e}")
        return {"error": str(e)}

# 6. STUDENT QUERY ROUTE (Ends in /query)
@app.post("/query")
async def ask_question(data: QueryData):
    system_instruction = "You are the Wheresmynotes Academic AI for Dibrugarh University."
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": data.question}
            ],
            model="llama-3.1-8b-instant",
        )
        return {"answer": completion.choices[0].message.content}
    except Exception as e:
        print(f"QUERY ERROR: {e}")
        return {"answer": f"Error: {str(e)}"}
