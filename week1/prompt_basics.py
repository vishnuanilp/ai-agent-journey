from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
task = "Analyze this business idea: an app that connects freelance chefs with busy families"

# STRATEGY 1 - Zero Shot
# Just ask directly, no examples
response1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": task}
    ]
)

# STRATEGY 2 - Few Shot
# Give examples first, then ask
response2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": """Here are examples of good business analysis:

Example 1:
Idea: An app that delivers groceries in 10 minutes
Analysis:
- Market: Busy urban professionals, parents
- Problem it solves: Time saving, convenience
- Risk: High delivery cost, thin margins
- Verdict: Viable in dense cities only

Example 2:
Idea: A platform connecting dog owners with local walkers
Analysis:
- Market: Working pet owners
- Problem it solves: Pet care during work hours
- Risk: Trust and safety concerns
- Verdict: Strong market, needs verification system

Now analyze this using the SAME format:
Idea: """ + task}
    ]
)
# STRATEGY 3 - Chain of Thought
# Ask it to think step by step before answering
response3 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": """Think step by step before giving your final answer.

Step 1: Who is the target customer?
Step 2: What exact problem does this solve?
Step 3: Who are the competitors?
Step 4: What are the biggest risks?
Step 5: What would make this succeed or fail?
Final: Give a clear verdict with one action to take immediately.

Now analyze this idea:
""" + task}
    ]
)

print("\n" + "=" * 50)
print("STRATEGY 2 - FEW SHOT")
print("=" * 50)
print(response2.choices[0].message.content)
