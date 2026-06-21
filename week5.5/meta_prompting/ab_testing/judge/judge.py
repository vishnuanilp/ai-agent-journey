import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv("../../.env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def judge_output(message, output):
    with open("judge_prompt.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()

    prompt = prompt_template.replace("{MESSAGE}", message).replace("{OUTPUT}", output)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text
    return json.loads(raw)

if __name__ == "__main__":
    test_message = "Paid 1500 for groceries today"
    test_output = '```json\n{"type": "payment_claim", "amount": 500}\n```'

    result = judge_output(test_message, test_output)
    print(json.dumps(result, indent=2))