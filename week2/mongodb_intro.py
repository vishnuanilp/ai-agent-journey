from dotenv import load_dotenv
import os
from anthropic import Anthropic
import anthropic
from pymongo import MongoClient
import datetime

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["ai_agent_db"]
collection = db["agent_results"]

print("MongoDB connected!")

# Save a document to MongoDB
def save_result(topic, step, content):
    document = {
        "topic": topic,
        "step": step,
        "content": content,
        "timestamp": datetime.datetime.now()
    }
    result = collection.insert_one(document)
    print(f"Saved! ID: {result.inserted_id}")
    return result.inserted_id

# Read all documents
def get_all_results():
    results = collection.find()
    for doc in results:
        print(f"\nTopic: {doc['topic']}")
        print(f"Step: {doc['step']}")
        print(f"Time: {doc['timestamp']}")

# Test saving
save_result(
    topic="AI agent for shops",
    step="research",
    content="Tier 2 cities have 150M consumers"
)

save_result(
    topic="AI agent for shops",
    step="article",
    content="Full article about AI for shops..."
)

print("\n--- ALL SAVED RESULTS ---")
get_all_results()

# Connect prompt chain to MongoDB
def run_pipeline_with_mongodb(topic):
    print(f"\n{'='*50}")
    print(f"Pipeline starting for: {topic}")
    print(f"{'='*50}")

    # Step 1 - Research
    print("\n🔍 Step 1: Researching...")
    research_prompt = f"""
<task>Research this topic and extract key facts</task>
<topic>{topic}</topic>
<rules>
- Find exactly 5 key facts
- Each fact must be specific and useful
- Keep each fact to one sentence
</rules>
<format>
Fact 1:
Fact 2:
Fact 3:
Fact 4:
Fact 5:
</format>
"""
    try:
        research_response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{"role": "user", "content": research_prompt}]
        )
        research = research_response.content[0].text
        save_result(topic, "research", research)
        print("✅ Research saved to MongoDB!")

    except Exception as e:
        print(f"❌ Research failed: {e}")
        return

    # Step 2 - Article
    print("\n✍️  Step 2: Writing article...")
    article_prompt = f"""
<task>Write a short article based on these facts</task>
<topic>{topic}</topic>
<research>{research}</research>
<rules>
- Write exactly 2 paragraphs
- Each paragraph maximum 3 sentences
- Professional but easy to read
- End with one actionable takeaway
</rules>
"""
    try:
        article_response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{"role": "user", "content": article_prompt}]
        )
        article = article_response.content[0].text
        save_result(topic, "article", article)
        print("✅ Article saved to MongoDB!")

    except Exception as e:
        print(f"❌ Article failed: {e}")
        return

    print(f"\n{'='*50}")
    print("FINAL ARTICLE:")
    print(f"{'='*50}")
    print(article)

# Run it!
run_pipeline_with_mongodb("AI agent for tier 2 shop owners")