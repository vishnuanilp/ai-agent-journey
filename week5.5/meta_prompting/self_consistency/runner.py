import os
import json
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-haiku-4-5"

PROMPT_TEMPLATE = Path("prompts/parser_v4_with_confidence.txt").read_text(encoding="utf-8")

def call_once(message: str, temperature: float = 0.4) -> dict:
    """Call Haiku once. Return parsed JSON dict."""
    prompt = PROMPT_TEMPLATE.replace("{MESSAGE}", message)

    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text.strip()
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    return json.loads(raw_text)

from concurrent.futures import ThreadPoolExecutor, as_completed


def call_n_parallel(message: str, n: int = 5, temperature: float = 0.4) -> list[dict]:
    """Call Haiku N times in parallel. Return list of N parsed JSON dicts."""
    results = []

    with ThreadPoolExecutor(max_workers=n) as executor:
        futures = [
            executor.submit(call_once, message, temperature)
            for _ in range(n)
        ]
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"⚠️  One call failed: {e}")

    return results

from collections import Counter


def majority_vote(results: list[dict], field: str = "message_type") -> tuple[str, int]:
    """Return the most common value of `field` across results, plus its vote count."""
    values = [r.get(field) for r in results if r.get(field) is not None]
    if not values:
        return ("ambiguous", 0)
    winner, count = Counter(values).most_common(1)[0]
    return (winner, count)

def parse_with_routing(message: str, threshold: int = 8) -> dict:
    """One call first. If confidence < threshold, fire 4 more and vote."""
    first = call_once(message, temperature=0.4)
    confidence = first.get("confidence", 0)

    if confidence >= threshold:
        print(f"✅ Confident ({confidence}). Skipping vote.")
        return {"answer": first, "votes": 1, "voted": False}

    print(f"⚠️  Low confidence ({confidence}). Firing 4 more...")
    extra = call_n_parallel(message, n=4, temperature=0.9)
    all_results = [first] + extra
    winner, count = majority_vote(all_results)

    return {
        "answer": {"message_type": winner, "confidence": confidence},
        "votes": count,
        "voted": True,
        "all_calls": all_results,
    }

if __name__ == "__main__":
    test_messages = [
        "mom said internet is 1500 this month",  # clear, expect skip
        "dad 2000",                              # vague, expect vote
        "electricity 800 ok",                    # ambiguous, expect vote
    ]

    for msg in test_messages:
        print("\n" + "=" * 70)
        print(f"📨 Testing: {msg!r}")
        print("=" * 70)
        result = parse_with_routing(msg)
        print(f"\n🎯 Final answer: {result['answer'].get('message_type')}")
        print(f"   Voted: {result['voted']}, votes: {result['votes']}/5")