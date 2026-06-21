import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-haiku-4-5"


TOT_PROMPT = """You are helping decide whether to cancel a recurring subscription.

The subscription in question:
{SUBSCRIPTION}

You MUST consider exactly three options before deciding:
1. CANCEL NOW
2. PAUSE FOR 3 MONTHS
3. KEEP IT

For each of the three options, produce:
- "case_for": one sentence describing who this option suits best
- "case_against": one sentence describing the main risk or downside
- "score": an integer from 1 to 10 reflecting how strong this option is

After evaluating all three, pick the option with the highest score as your final recommendation.

Return ONLY a single JSON object in this exact shape (no markdown fences, no prose):

{
  "branches": [
    {"option": "CANCEL NOW", "case_for": "...", "case_against": "...", "score": 0},
    {"option": "PAUSE FOR 3 MONTHS", "case_for": "...", "case_against": "...", "score": 0},
    {"option": "KEEP IT", "case_for": "...", "case_against": "...", "score": 0}
  ],
  "final_pick": "<one of CANCEL NOW | PAUSE FOR 3 MONTHS | KEEP IT>",
  "reason": "<one sentence explaining why this option won>"
}
"""


def run_tot(subscription: str) -> dict:
    """Send one TOT prompt to Haiku. Return parsed tree + final pick."""
    prompt = TOT_PROMPT.replace("{SUBSCRIPTION}", subscription)

    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    return json.loads(raw)


def print_tree(result: dict) -> None:
    """Pretty-print the TOT result so you can see Haiku's reasoning."""
    print("\n🌳 Tree of Thought\n")
    for branch in result.get("branches", []):
        print(f"  ── {branch['option']}  (score: {branch['score']})")
        print(f"       ✅ For:     {branch['case_for']}")
        print(f"       ⚠️  Against: {branch['case_against']}")
        print()

    print(f"🎯 Final pick: {result['final_pick']}")
    print(f"   Reason:    {result['reason']}")


if __name__ == "__main__":
    subscription = "Netflix Premium, €18/month. Used about 4 hours last month. Family of 3 sharing the account but only one watches regularly."

    print(f"📺 Subscription: {subscription}\n")
    print("=" * 70)

    result = run_tot(subscription)
    print_tree(result)