from dotenv import load_dotenv
import os
from openai import OpenAI
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Lesson 4 - Output Formatting ready!")

# Prompt template for business idea analysis
def analyze_business_idea(idea):
    prompt = f"""
    Analyze this business idea CRITICALLY and honestly.
    Respond ONLY in JSON format. No extra text.
    
    Business idea: {idea}
    
    Scoring rules:
    - 1 to 3 = bad idea, very high risk, small market
    - 4 to 6 = average idea, needs major improvements  
    - 7 to 8 = good idea, viable with some risks
    - 9 to 10 = exceptional idea, rare to score this high
    
    Be strict. Most ideas score between 5 and 7.
    
    Respond in exactly this format:
    {{
        "verdict": "Viable or Not Viable",
        "market_size": "Large, Medium, or Small",
        "top_risk": "the biggest single risk",
        "top_opportunity": "the biggest single opportunity",
        "action": "one specific action to take this week",
        "score": a number from 1 to 10
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Get the raw text response
    raw = response.choices[0].message.content
    
    # Convert JSON text into Python dictionary
    result = json.loads(raw)
    
    return result

# Test it
idea = "AN image generator that creates custom images for social media posts based on trending topics and user preferences"
print("Analyzing business idea...")
result = analyze_business_idea(idea)

print("\n--- RESULTS ---")
print(f"Verdict:     {result['verdict']}")
print(f"Market Size: {result['market_size']}")
print(f"Top Risk:    {result['top_risk']}")
print(f"Opportunity: {result['top_opportunity']}")
print(f"Action:      {result['action']}")
print(f"Score:       {result['score']}/10")

