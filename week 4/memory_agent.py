import os
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic
from pymongo import MongoClient

load_dotenv()
client = Anthropic()
mongo = MongoClient("mongodb://localhost:27017/")
db = mongo["memory_agent"]
memories = db["user_memories"]

def save_memory(fact):
    memories.insert_one({
        "fact": fact,
        "timestamp": datetime.now()
    })

def load_memories():
    facts = []
    for doc in memories.find():
        facts.append(doc["fact"])
    return facts

def extract_memory(user_message):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        temperature=0,
        messages=[{
            "role": "user",
            "content": f"""Read this user message and decide if it contains a fact worth remembering long-term about the user (like their name, location, preferences, job, etc).

If YES, respond with ONLY the fact in one short sentence starting with "User".
If NO, respond with ONLY the word: nothing

User message: {user_message}"""
        }]
    )

    result = response.content[0].text.strip()
    if result.lower() != "nothing":
        save_memory(result)

def chat():
    saved_facts = load_memories()
    system_prompt = "You are a helpful assistant."
    if saved_facts:
        system_prompt += "\n\nWhat you remember about the user:\n- " + "\n- ".join(saved_facts)

    messages = []
    print("Chat started. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower().strip() == "quit":
            break

        messages.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )

        reply = response.content[0].text
        messages.append({"role": "assistant", "content": reply})
        print(f"Assistant: {reply}\n")

        extract_memory(user_input)

if __name__ == "__main__":
    chat()