import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
client = Anthropic()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Vishnu!"}

class Lead(BaseModel):
    name: str
    email: str
    company: str
    budget: int
    message: str

@app.post("/qualify-lead")
def qualify_lead(lead: Lead):
    prompt = f"""Score this lead 1-10 and give one reason.

Lead details:
- Name: {lead.name}
- Company: {lead.company}
- Budget: ${lead.budget}
- Message: {lead.message}

Return ONLY a raw JSON object like: {{"score": 8, "reason": "Strong budget and clear need"}}
Do NOT wrap it in markdown code fences (no ```json or ``` markers).
Return only the JSON object, nothing else."""
    
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    claude_text = response.content[0].text
    
    # Defense #2: strip markdown fences if Claude included them
    cleaned = claude_text.replace("```json", "").replace("```", "").strip()
    
    # Parse the cleaned string into a real Python dict
    result = json.loads(cleaned)
    
    return result