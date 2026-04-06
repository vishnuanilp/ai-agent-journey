import anthropic
from anthropic import Anthropic
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
client = Anthropic()
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["week2_agents"]
collection = db["pipeline_results"]
collection.delete_many({})

def call_claude(system, prompt, step_name):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": prompt}]
        )
        print(f"== {step_name} ==")
        print(response.content[0].text)
        return response.content[0].text
    except Exception as e:
        print(f"{step_name} failed: {e}")
        return None

def save_to_mongo(step_name, topic, result):
    doc = {
        "step": step_name,
        "topic": topic,
        "result": result,
        "timestamp": datetime.now().isoformat()
    }
    collection.insert_one(doc)
    print(f"Saved {step_name} to MongoDB!")

topic = "How AI is changing small businesses in 2025"

result1 = call_claude(
    "You are a research assistant. Find key facts only.",
    f"""<task>Research key facts about this topic</task>
    <topic>{topic}</topic>
    <rules>Return exactly 5 key facts</rules>
    <format>A numbered list of 5 facts</format>""",
    "Step 1: Research"
)
if result1:
    save_to_mongo("research", topic, result1)

result2 = None
if result1:
    result2 = call_claude(
        "You are an outline specialist.",
        f"""<task>Outline a report based on these facts</task>
        <facts>{result1}</facts>
        <rules>Introduction, 3 main sections, conclusion</rules>
        <format>An outline with headings and bullet points</format>""",
        "Step 2: Outline"
    )
    if result2:
        save_to_mongo("outline", topic, result2)

result3 = None
if result2:
    result3 = call_claude(
        "You are a professional blog writer.",
        f"""<task>Write a report based on this outline</task>
        <outline>{result2}</outline>
        <rules>Clear, engaging style. 2-3 sentences per point.</rules>
        <format>A well-written report</format>""",
        "Step 3: Write"
    )
    if result3:
        save_to_mongo("write", topic, result3)

result4 = None
if result3:
    result4 = call_claude(
        "You are a professional editor.",
        f"""<task>Edit this report for clarity and style</task>
        <report>{result3}</report>
        <rules>Fix grammar, improve flow, make engaging</rules>
        <format>A polished, final version</format>""",
        "Step 4: Edit"
    )
    if result4:
        save_to_mongo("edit", topic, result4)

print("\n== All saved results ==")
for doc in collection.find():
    print(f"{doc['step']} - {doc['timestamp']}")
    
