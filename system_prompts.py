from dotenv import load_dotenv
import os
from openai import OpenAI
import sqlite3
import datetime
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
conn = sqlite3.connect("conversations.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        persona TEXT,
        role TEXT,
        content TEXT
    )
""")
conn.commit()
print("Database created successfully!")
# Define 3 different personas using system prompts
personas = {
    "consultant": """You are a professional business consultant with 20 years 
    of experience. You speak formally, use business terminology, and always 
    focus on ROI, market analysis, and strategic growth. Be direct and 
    data-driven in your responses.""",
    
    "mentor": """You are a warm and friendly mentor who genuinely cares about 
    helping people succeed. You use simple language, give encouragement, share 
    personal stories, and always end with a motivating message.""",
    
    "critic": """You are a tough but fair critic. You challenge every idea, 
    point out weaknesses, ask hard questions, and never accept vague answers. 
    Your job is to make ideas stronger by stress-testing them."""
}

print("Personas defined!")
print(f"Number of personas: {len(personas)}")

def save_message(persona, role, content):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO messages (timestamp, persona, role, content)
        VALUES (?, ?, ?, ?)
    """, (timestamp, persona, role, content))
    conn.commit()
    print(f"Saved: [{persona}] {role}: {content[:50]}...")

    # The test message we send to all 3 personas
test_message = "I want to start an AI business. What should I do first?"

print("\n" + "="*60)
print("SENDING SAME MESSAGE TO ALL 3 PERSONAS")
print("="*60)
print(f"Message: {test_message}\n")

# Loop through each persona
for persona_name, system_prompt in personas.items():
    
    # Save user message to database
    save_message(persona_name, "user", test_message)
    
    # Send to OpenAI with the persona's system prompt
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": test_message}
        ]
    )
    
    reply = response.choices[0].message.content
    
    # Save AI response to database
    save_message(persona_name, "assistant", reply)
    
    # Print the result
    print(f"\n{'='*60}")
    print(f"PERSONA: {persona_name.upper()}")
    print(f"{'='*60}")
    print(reply)
