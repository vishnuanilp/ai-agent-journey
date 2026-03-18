from dotenv import load_dotenv
import os
from anthropic import Anthropic
import anthropic
import time

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def call_claude(prompt, step_name, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        except anthropic.RateLimitError:
            wait_time = 2 ** attempt
            print(f"{step_name} rate limited! Waiting {wait_time}s...")
            time.sleep(wait_time)

        except anthropic.AuthenticationError:
            print(f"{step_name} auth error! Check API key.")
            return None

        except Exception as e:
            print(f"{step_name} failed attempt {attempt+1}: {e}")
            time.sleep(2)

    return None

# Step 1 — Research Agent
def research_agent(topic):
    print(f"\n🔍 Step 1: Researching '{topic}'...")
    
    prompt = f"""
<task>Research this topic and extract key facts</task>

<topic>{topic}</topic>

<rules>
- Find exactly 5 key facts
- Each fact must be specific and useful
- Focus on facts that would help write an article
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
    result = call_claude(prompt, "Research Agent")
    if result:
        print("✅ Research complete!")
        return result
    return None

# Step 2 — Outline Agent
def outline_agent(topic, research):
    print(f"\n📝 Step 2: Creating outline...")
    
    prompt = f"""
<task>Create a structured article outline</task>

<topic>{topic}</topic>

<research>
{research}
</research>

<rules>
- Create exactly 3 main sections
- Each section needs a title and 2 key points
- Use the research facts provided
- Keep it focused and practical
</rules>

<format>
Section 1: [Title]
- Point 1:
- Point 2:

Section 2: [Title]
- Point 1:
- Point 2:

Section 3: [Title]
- Point 1:
- Point 2:
</format>
"""
    result = call_claude(prompt, "Outline Agent")
    if result:
        print("✅ Outline complete!")
        return result
    return None

# Step 3 — Writer Agent
def writer_agent(topic, outline):
    print(f"\n✍️  Step 3: Writing article...")
    
    prompt = f"""
<task>Write a short article based on this outline</task>

<topic>{topic}</topic>

<outline>
{outline}
</outline>

<rules>
- Write exactly 3 paragraphs — one per section
- Each paragraph maximum 3 sentences
- Professional but easy to read tone
- End with one actionable takeaway
</rules>
"""
    result = call_claude(prompt, "Writer Agent")
    if result:
        print("✅ Article complete!")
        return result
    return None

# Run the full pipeline
def run_pipeline(topic):
    print(f"\n{'='*50}")
    print(f"Starting Content Pipeline for: {topic}")
    print(f"{'='*50}")
    
    # Step 1
    research = research_agent(topic)
    if not research:
        print("❌ Pipeline failed at Step 1")
        return
    
    # Step 2 — uses Step 1 output
    outline = outline_agent(topic, research)
    if not outline:
        print("❌ Pipeline failed at Step 2")
        return
    
    # Step 3 — uses Step 2 output
    article = writer_agent(topic, outline)
    if not article:
        print("❌ Pipeline failed at Step 3")
        return
    
    print(f"\n{'='*50}")
    print("FINAL ARTICLE:")
    print(f"{'='*50}")
    print(article)

# Test it
run_pipeline("food delivery app")
run_pipeline("AI agent for tier 2 shop owners in India")
