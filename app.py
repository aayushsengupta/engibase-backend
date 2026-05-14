import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

app = FastAPI()

# 2. CORS Setup (Essential for Vercel/Frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Initialize Groq Client
# It looks for "GROQ_API_KEY" in Render's environment or your local .env file
# Replace 'YOUR_NEW_KEY_HERE' with your key if testing locally without .env
api_key = os.environ.get("GROQ_API_KEY", "YOUR_NEW_KEY_HERE")
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

# 5. RESUME ROUTE
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
        return {"resume": completion.choices[0].message.content}
    except Exception as e:
        print(f"RESUME ERROR: {e}")
        return {"error": str(e)}

# 6. STUDENT QUERY ROUTE
@app.post("/query")
async def ask_question(data: QueryData):
    # Customized for your university context
    system_instruction = "You are the Wheresmynotes Academic AI for Dibrugarh University."
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": data.question}
            ],
        )
        return {"answer": completion.choices[0].message.content}
    except Exception as e:
        print(f"QUERY ERROR: {e}")
        return {"answer": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    # Use port 10000 for Render compatibility
    uvicorn.run(app, host="0.0.0.0", port=10000)
