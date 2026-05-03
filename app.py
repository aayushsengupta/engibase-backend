from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# THIS BLOCK IS THE FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # This allows the site on 5500 to talk to port 8000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key="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")

class ResumeRequest(BaseModel):
    name: str
    email: str
    skills: str
    experience: str
    education: str

class ResumeData(BaseModel):
    name: str
    email: str
    skills: str
    experience: str
    education: str

@app.post("/generate")
async def generate(data: ResumeData):
    # This is the "Magic" prompt that tells Llama how to behave
    prompt = f"""
    You are an expert resume builder. Create a professional, clean resume based on these details:
    NAME: {data.name}
    EMAIL: {data.email}
    SKILLS: {data.skills}
    EXPERIENCE: {data.experience}
    EDUCATION: {data.education}
    
    Format the output clearly using Markdown. Use bold headers and bullet points. 
    Keep it professional and ready for a job application.
    """

    try:
        # Calling the Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant", # Using the fast Llama 3 model
        )
        
        # This sends the AI's actual text back to your website
        return {"markdown": chat_completion.choices[0].message.content}
        
    except Exception as e:
        print(f"TERMINAL ERROR: {e}") # This forces it to show up in the black box
        return {"markdown": f"Generation failed: {str(e)}"}
    
class QueryData(BaseModel):
    question: str

# The Knowledge Map based on your provided data
MODULE_KNOWLEDGE_BASE = {
    "General Engineering": [
        "Mathematics-I & II", "Basic Electrical Engineering", "Engineering Graphics & Design",
        "English for Technical Writing", "Biology for Engineers", "Design Thinking", "Physics-I", "Chemistry"
    ],
    "Petroleum Engineering": [
        "Engineering Geology", "Petroleum Geology", "Thermodynamics for Petroleum Engineers",
        "Fluid Mechanics", "Reservoir Engineering (Elements & Applied)", "Drilling Technology I & II",
        "Production Engineering I & II", "Well Logging", "Natural Gas Engineering", "Petroleum Refinery",
        "Enhanced Oil Recovery (EOR)", "Well Test Analysis", "Pipeline Engineering"
    ],
    "Computer Science (CSE)": [
        "Data Structures & Algorithms", "Operating Systems", "Database Management Systems (DBMS)",
        "Computer Networks", "Artificial Intelligence", "Machine Learning", "Cloud Computing",
        "Cyber Security", "Internet of Things (IoT)"
    ],
    "Electronics (ECE)": [
        "Electronic Devices", "Digital System Design", "Signals and Systems", "Network Theory",
        "Analog Circuits", "Microprocessors", "Digital Signal Processing", "VLSI Design", "Fiber Optics"
    ],
    "Mechanical Engineering": [
        "Thermodynamics", "Applied Thermodynamics", "Strength of Materials", "Manufacturing Processes",
        "Heat & Mass Transfer", "Machine Design", "Dynamics of Machinery", "CAD/CAM", "Refrigeration & AC"
    ]
}

@app.post("/query")
async def ask_question(data: QueryData):
    # This 'System Instruction' tells the AI exactly what it knows
    system_instruction = f"""
    You are the 'Wheresmynotes' Academic AI. You provide tutoring for students at Dibrugarh University.
    
    You have access to the following module categories and subjects:
    {MODULE_KNOWLEDGE_BASE}
    
    When answering:
    1. Identify which module the question belongs to.
    2. Provide a clear, engineering-focused explanation.
    3. If the question is outside these modules, answer generally but mention it's not in the primary vault.
    """

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
        return {"answer": f"Error: {str(e)}"}

@app.post("/query")
async def ask_question(data: QueryData):
    prompt = f"You are a specialized academic assistant for Wheresmynotes. Answer this student's question based on engineering modules: {data.question}"
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant", # Using the new stable model
        )
        return {"answer": completion.choices[0].message.content}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
    
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This is the "Universal Permission" block
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your local 127.0.0.1 and Netlify
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-resume")
async def generate_resume(request: ResumeRequest):
    try:
        # 1. Check if the prompt construction is clean
        user_prompt = f"Create a resume for {request.name}. Skills: {request.skills}."

        # 2. Use the ACTIVE model name
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        return {"resume": completion.choices[0].message.content}
    except Exception as e:
        # This will print the actual error in your Render logs if it fails
        print(f"CRITICAL ERROR: {e}")
        return {"error": str(e)}
    return {"resume": chat_completion.choices[0].message.content}
