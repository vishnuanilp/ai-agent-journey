import json
import os
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv
from ab_test import call_claude, score, cases

from optimizer import (
    make_xml_variant,
    make_cot_variant,
    make_fewshot_variant,
    make_role_variant,
    make_meta_variant,
)
from ab_test import call_claude, score, cases

load_dotenv("../.env")
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("Loading starting prompt (v4b)...")
with open("prompts/v4b_no_confidence.txt", "r", encoding="utf-8") as f:
    starting_prompt = f.read()

print(f"Starting prompt: {len(starting_prompt)} chars\n")

# Map of strategy name → function
strategies = {
    "cot": make_cot_variant,
    "fewshot": make_fewshot_variant,
    "role": make_role_variant,
    "xml": make_xml_variant,
    "meta": make_meta_variant,
}

candidates = {}
for name, fn in strategies.items():
    print(f"Generating {name} variant...")
    variant_text = fn(starting_prompt)
    candidates[name] = variant_text
    
    filename = f"prompts/candidate_{name}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(variant_text)
    print(f"  → Saved {len(variant_text)} chars to {filename}")

print(f"\n✓ All 5 candidates generated and saved to prompts/")

print(f"\n{'='*60}\nSCORING ALL 5 CANDIDATES\n{'='*60}")

arena_results = {}

for name, prompt_text in candidates.items():
    print(f"\nScoring '{name}' variant...")
    case_results = []
    total_score = 0
    total_max = 0
    
    for case in cases:
        actual = call_claude(prompt_text, case["message"])
        s = score(actual, case["expected"])
        case_results.append({"id": case["id"], "score": s, "actual": actual})
        total_score += s["total"]
        total_max += s["max"]
    
    accuracy = 100 * total_score / total_max
    arena_results[name] = {
        "total_score": total_score,
        "total_max": total_max,
        "accuracy_pct": round(accuracy, 1),
        "case_results": case_results,
    }
    print(f"  {name}: {total_score}/{total_max} ({accuracy:.1f}%)")


print(f"\n{'='*60}\nFINAL RESULTS\n{'='*60}\n")

ranked = sorted(arena_results.items(), key=lambda kv: kv[1]["total_score"], reverse=True)
for rank, (name, data) in enumerate(ranked, start=1):
    print(f"  {rank}. {name:8} {data['total_score']}/{data['total_max']}  ({data['accuracy_pct']}%)")

winner_name, winner_data = ranked[0]
print(f"\nBest candidate: '{winner_name}' at {winner_data['accuracy_pct']}%")
print(f"Baseline v4b (yesterday): 39/42 (92.9%)")

if winner_data["total_score"] > 39:
    print(f"\n✓ Winner beats baseline. Recommend promoting '{winner_name}' to champion.")
elif winner_data["total_score"] == 39:
    print(f"\n~ Tie with baseline. v4b stays champion (Occam's razor: simpler wins on ties).")
else:
    print(f"\n✗ No candidate beats baseline. v4b stays champion.")