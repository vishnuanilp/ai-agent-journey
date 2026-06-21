import json

with open("test_inputs.json", "r", encoding="utf-8") as f:
    cases = json.load(f)

print(f"Loaded {len(cases)} test cases")