import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv("../.env")
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Load both prompts
with open("prompts/v4_with_confidence.txt", "r", encoding="utf-8") as f:
    prompt_v4 = f.read()

with open("prompts/v4b_no_confidence.txt", "r", encoding="utf-8") as f:
    prompt_v4b = f.read()

# Load test cases
with open("test_inputs.json", "r", encoding="utf-8") as f:
    cases = json.load(f)

print(f"v4 prompt:  {len(prompt_v4)} chars")
print(f"v4b prompt: {len(prompt_v4b)} chars")
print(f"Test cases: {len(cases)}\n")


def call_claude(prompt_template, message):
    """Run one message through one prompt. Return parsed JSON dict."""
    full_prompt = prompt_template.replace("{MESSAGE}", message)
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        temperature=0,
        messages=[{"role": "user", "content": full_prompt}]
    )
    raw_text = response.content[0].text
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"_parse_error": True, "raw": cleaned}


def score(actual, expected):
    """Score one response. Returns dict of field-level matches."""
    if actual.get("_parse_error"):
        return {"message_type": 0, "bill_name": 0, "amount": 0, "total": 0}
    
    result = {}
    # message_type — always scored
    result["message_type"] = 1 if actual.get("message_type") == expected.get("message_type") else 0
    
    # bill_name — only scored if expected has it
    if "bill_name" in expected:
        result["bill_name"] = 1 if actual.get("bill_name") == expected.get("bill_name") else 0
    else:
        result["bill_name"] = None  # not applicable
    
    # amount — only scored if expected has it
    if "amount" in expected:
        result["amount"] = 1 if actual.get("amount") == expected.get("amount") else 0
    else:
        result["amount"] = None  # not applicable
    
    # total = sum of applicable fields
    scored = [v for v in result.values() if v is not None]
    result["total"] = sum(scored)
    result["max"] = len(scored)
    return result


def run_test(prompt, label):
    """Run all 20 cases through one prompt. Return total score and details."""
    print(f"\n{'='*60}\nRunning {label}\n{'='*60}")
    results = []
    total_score = 0
    total_max = 0
    
    for case in cases:
        actual = call_claude(prompt, case["message"])
        s = score(actual, case["expected"])
        results.append({"id": case["id"], "message": case["message"], "actual": actual, "score": s})
        total_score += s["total"]
        total_max += s["max"]
        status = "✓" if s["total"] == s["max"] else "✗"
        print(f"  {status} Case {case['id']:>2}: {s['total']}/{s['max']}  | {case['message'][:40]}")
    
    return total_score, total_max, results


# Run both prompts
if __name__ == "__main__":
    # Run both prompts
    v4_score, v4_max, v4_results = run_test(prompt_v4, "v4 (with confidence)")
    v4b_score, v4b_max, v4b_results = run_test(prompt_v4b, "v4b (no confidence)")

    # Declare winner
    print(f"\n{'='*60}\nFINAL RESULTS\n{'='*60}")
    print(f"v4  (with confidence): {v4_score}/{v4_max}  ({100*v4_score/v4_max:.1f}%)")
    print(f"v4b (no confidence):   {v4b_score}/{v4b_max}  ({100*v4b_score/v4b_max:.1f}%)")

    if v4_score > v4b_score:
        print(f"\n🏆 WINNER: v4 (confidence helps by {v4_score - v4b_score} points)")
    elif v4b_score > v4_score:
        print(f"\n🏆 WINNER: v4b (confidence HURTS by {v4b_score - v4_score} points — drop it)")
    else:
        print(f"\n🤝 TIE — confidence has no impact; drop it for simpler output")