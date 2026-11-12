from vocmem import app
from nodes import answer
hits = app.get_state({"configurable": {"thread_id": "c1"}}).values["hits"]
QS = [
    "What is the hotel's policy on bringing cats?",   # today's rewrite
    "Can I bring my cat to the hotel?",               # Friday's rewrite
    "what about cats?",                               # raw follow-up
]
for q in QS:
    replies = [answer({"question": q, "hits": hits})["answer"] for _ in range(5)]
    yes = sum("know" not in r.lower() for r in replies)
    print(f"{yes}/5 answered | {q}")
    for r in sorted(set(replies)):
        print("     ", r[:110])