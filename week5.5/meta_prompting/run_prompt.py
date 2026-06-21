
"""Run any prompt version against all test inputs and save the results."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    sys.exit("ERROR: ANTHROPIC_API_KEY not found in .env")

if len(sys.argv) < 2:
    sys.exit("Usage: python run_prompt.py <prompt_version>\nExample: python run_prompt.py v1")

version = sys.argv[1]
prompt_path = Path("prompts") / f"prompt_{version}.txt"

if not prompt_path.exists():
    sys.exit(f"ERROR: {prompt_path} not found")

prompt_template = prompt_path.read_text(encoding="utf-8")

test_inputs_path = Path("test_inputs.txt")
test_messages = test_inputs_path.read_text(encoding="utf-8").splitlines()
test_messages = [m.strip() for m in test_messages if m.strip()]

print(f"Loaded prompt: {prompt_path}")
print(f"Loaded {len(test_messages)} test messages")

client = Anthropic(api_key=api_key)

results = []

for i, message in enumerate(test_messages):
    print(f"\n[{i+1}/{len(test_messages)}] Input: {message}")

    filled_prompt = prompt_template.replace("{MESSAGE}", message)

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        temperature=0,
        messages=[{"role": "user", "content": filled_prompt}],
    )
    output = response.content[0].text

    print(f"Output: {output}")
    results.append({"input": message, "output": output})
