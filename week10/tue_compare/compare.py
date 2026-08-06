from runners import ask_openai, ask_claude, ask_gemini, parse

FRAMES = {"room_person": 1, "room_empty": 0,
          "room_dark": 0, "street_crowd": 9}
MODELS = [("openai", ask_openai), ("claude", ask_claude),
          ("gemini", ask_gemini)]

for fname, truth in FRAMES.items():
    print(f"\n== {fname} (truth: {truth}) ==")
    for mname, fn in MODELS:
        for run in range(3):
            text, secs = fn(f"frames/{fname}.jpg")
            d = parse(text)
            print(f"{mname:8} run{run+1} {secs:4.1f}s "
                  f"present={d['person_present']} count={d['person_count']}")