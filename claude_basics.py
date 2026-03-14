from dotenv import load_dotenv
import os
from openai import OpenAI
from anthropic import Anthropic

load_dotenv()

# Both clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Test question
question = "What are the top 3 skills an AI startup founder needs?"

# OpenAI response
openai_response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": question}]
)
openai_reply = openai_response.choices[0].message.content

# Claude response
claude_response = claude_client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1000,
    messages=[{"role": "user", "content": question}]
)
claude_reply = claude_response.content[0].text

print("=" * 50)
print("OPENAI REPLY:")
print(openai_reply)
print("=" * 50)
print("CLAUDE REPLY:")
print(claude_reply)
print("=" * 50)