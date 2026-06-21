import os
import json
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic
from judge import judge_output

load_dotenv("../../.env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def run_candidate(prompt_text, message):
    filled_prompt = prompt_text.replace("{MESSAGE}", message)

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": filled_prompt}]
    )

    return response.content[0].text


candidates = {
    "v4b_no_confidence": open("../prompts/v4b_no_confidence.txt").read(),
    "candidate_xml":     open("../prompts/candidate_xml.txt").read(),
}

with open("../test_inputs.json", "r", encoding="utf-8") as f:
    test_cases = json.load(f)

messages = [case["message"] for case in test_cases]


if __name__ == "__main__":
    run_record = {
        "run_id": f"judge_arena_{datetime.now().strftime('%Y-%m-%d_%H-%M')}",
        "judge_model": "claude-sonnet-4-6",
        "candidate_model": "claude-haiku-4-5",
        "temperature": 0,
        "test_message_count": len(messages),
        "candidates": {},
    }

    for name, prompt_text in candidates.items():
        print(f"\n========== Running candidate: {name} ==========")
        per_message = []
        running_total = 0

        for i, message in enumerate(messages, start=1):
            output = run_candidate(prompt_text, message)
            scores = judge_output(message, output)
            total = scores["accuracy"] + scores["relevance"] + scores["format"]
            running_total += total
            per_message.append({
                "message": message,
                "output": output,
                "scores": scores,
                "total": total,
            })
            print(f"  [{i}/{len(messages)}] {total}/15 — {message[:50]}")

        run_record["candidates"][name] = {
            "total": running_total,
            "max_possible": len(messages) * 15,
            "per_message": per_message,
        }

    print("\n========== FINAL RANKINGS ==========")
    ranked = sorted(
        run_record["candidates"].items(),
        key=lambda r: r[1]["total"],
        reverse=True,
    )
    max_possible = len(messages) * 15
    for rank, (name, data) in enumerate(ranked, start=1):
        print(f"{rank}. {name} — {data['total']}/{max_possible}")

    winner_name, winner_data = ranked[0]
    runner_up_name, runner_up_data = ranked[1]
    margin = winner_data["total"] - runner_up_data["total"]

    if margin == 0:
        verdict = "tie"
        print(f"\n🤝 TIE: {winner_name} and {runner_up_name} both scored {winner_data['total']}/{max_possible}")
    elif margin <= 3:
        verdict = "tie_within_noise"
        print(f"\n⚠️  NEAR-TIE: {winner_name} won by {margin} point(s) — within noise floor, treat as tie")
    else:
        verdict = "clear_winner"
        print(f"\n🏆 WINNER: {winner_name} ({winner_data['total']}/{max_possible}, +{margin} over runner-up)")

    run_record["verdict"] = verdict
    run_record["winner"] = winner_name
    run_record["margin"] = margin

    out_path = f"results/{run_record['run_id']}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(run_record, f, indent=2, ensure_ascii=False)
    print(f"\n📝 Saved run to: {out_path}")