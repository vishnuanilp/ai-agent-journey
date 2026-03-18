from dotenv import load_dotenv
import os
from anthropic import Anthropic
import anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("XML Tags lesson ready!")

# Normal prompt — no XML tags
normal_prompt = "You are a business analyst. Analyze this business idea: AI agent for tier 2 shop owners. Give me verdict, score and top risk."

# XML tags prompt — structured and clear
xml_prompt = """
<task>Analyze this business idea and provide structured feedback</task>

<persona>
You are an expert business analyst with 15 years experience
evaluating startups. Be honest and direct — never flatter bad ideas.
</persona>

<idea>
AI agent for tier 2 shop owners in India.
Simple chat interface that helps them manage their business.
Monthly subscription model.
</idea>

<rules>
- Score strictly between 1-10 (most ideas score 5-7)
- Identify the single biggest risk
- Give one specific action for this week
- Be concise — maximum 100 words
</rules>

<format>
Verdict: Viable or Not Viable
Score: X/10
Top Risk: one sentence
Opportunity: one sentence
Action: one specific action this week
</format>
"""

# Send both to Claude
print("--- NORMAL PROMPT ---")
normal_response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=500,
    messages=[{"role": "user", "content": normal_prompt}]
)
print(normal_response.content[0].text)

print("\n--- XML TAGS PROMPT ---")
xml_response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=500,
    messages=[{"role": "user", "content": xml_prompt}]
)
print(xml_response.content[0].text)