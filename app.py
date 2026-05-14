import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Essential for the frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CRITICAL FIX START ---
# Only initialize the client ONCE at the top level.
# This ensures every function uses the key from Render's Environment Variables.
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)
# --- CRITICAL FIX END ---

class ResumeRequest(BaseModel):
    name: str
    email: str
    skills: str
    experience: str
    education: str

class QueryData(BaseModel):
    question: str

@app.post("/generate-resume")
async def generate_resume(request: ResumeRequest):
    try:
        # Uses the 'client' defined above
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": f"Create a resume for {request.name}..."}]
        )
        return {"resume": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.post("/query")
async def ask_question(data: QueryData):
    # This function should ONLY use the 'client' defined at the top of the file
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Use the EXACT same model as the resume
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": data.question}
            ],
        )
        return {"answer": completion.choices[0].message.content}
    except Exception as e:
        # If it still fails, this will show the error in your Render logs
        print(f"QUERY FAIL: {str(e)}")
        return {"answer": f"Error: {str(e)}"}
