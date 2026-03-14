from dotenv import load_dotenv
import os
from openai import OpenAI
import sqlite3
import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database setup
conn = sqlite3.connect("conversations.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        role TEXT,
        content TEXT
    )
""")
conn.commit()

# System prompt
messages = [
    {"role": "system", "content": "You are a helpful AI assistant for entrepreneurs. Give practical actionable advice. Keep responses concise and clear."}
]

def save_message(role, content):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO chat_history (timestamp, role, content)
        VALUES (?, ?, ?)
    """, (timestamp, role, content))
    conn.commit()

print("AI Assistant ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        print("Goodbye!")
        break
    
    messages.append({"role": "user", "content": user_input})
    save_message("user", user_input)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    
    messages.append({"role": "assistant", "content": reply})
    save_message("assistant", reply)
    
    print(f"AI: {reply}\n")