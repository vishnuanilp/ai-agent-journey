"""Send a v1 prompt through the meta-prompt template and save the improved version."""

import os
import sys
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    sys.exit("ERROR: ANTHROPIC_API_KEY not found in .env")

# Which version are we improving FROM, and saving TO?
source_version = "v2"
target_version = "v3"

source_path = Path("prompts") / f"prompt_{source_version}.txt"
target_path = Path("prompts") / f"prompt_{target_version}.txt"
template_path = Path("meta_prompt_template.txt")

if not source_path.exists():
    sys.exit(f"ERROR: {source_path} not found")
if not template_path.exists():
    sys.exit(f"ERROR: {template_path} not found")

original_prompt = source_path.read_text(encoding="utf-8")
template = template_path.read_text(encoding="utf-8")
today_str = date.today().isoformat()

filled_meta_prompt = template.replace("{ORIGINAL_PROMPT}", original_prompt).replace("{TODAY}", today_str)

print(f"Source: {source_path}")
print(f"Target: {target_path}")
print(f"Today: {today_str}")
print(f"Sending {len(filled_meta_prompt)} chars to Sonnet...")

client = Anthropic(api_key=api_key)

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4000,
    temperature=0.3,
    messages=[{"role": "user", "content": filled_meta_prompt}],
)

improved_prompt = response.content[0].text

target_path.write_text(improved_prompt, encoding="utf-8")

print(f"\n✅ Improved prompt saved to: {target_path}")
print(f"   Length: {len(improved_prompt)} chars")