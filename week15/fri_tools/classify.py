import rag

LABELS = ("question", "action", "chitchat")
PROMPT = ("You label messages sent to a hotel. Reply with exactly ONE word: "
          "question (asks for information), action (wants something done, "
          "like booking), or chitchat (greeting, thanks, small talk).\n\nMessage: ")

def classify(msg):
    r = rag.oa.chat.completions.create(model="gpt-4o-mini", temperature=0,
        messages=[{"role": "user", "content": PROMPT + msg}])
    word = r.choices[0].message.content.strip().lower().strip(".")
    return word if word in LABELS else "unknown"

if __name__ == "__main__":
    tests = [("can I bring my dog?", "question"), ("do you sell mobile phones?", "question"),
             ("which room has a sea view?", "question"), ("book me a room for Saturday", "action"),
             ("thanks, you're great!", "chitchat")]
    for m, want in tests:
        got = classify(m)
        print(f"{m:30} want {want:9} got {got:9} {'OK' if got == want else 'WRONG'}")