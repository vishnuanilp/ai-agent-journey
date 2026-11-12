from vocmem import app
import rag
from ans_prompts import PROMPTS
hits = app.get_state({"configurable": {"thread_id": "c1"}}).values["hits"]
context = "\n".join(t for _, t, _ in hits)
def ask(q):
    msg = f"{PROMPTS['A2']}Context:\n{context}\n\nQuestion: {q}"
    r = rag.oa.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": msg}])
    return r.choices[0].message.content
for q, want in [("What is the hotel's policy on bringing cats?", "ANSWER"), ("Is late check-out available?", "REFUSE")]:
    rs = [ask(q) for _ in range(10)]
    bad = [r for r in rs if ("know" in r.lower()) != (want == "REFUSE")]
    print(f"A2 | {10 - len(bad)}/10 | want {want} | {q}")
    for r in sorted(set(bad)):
        print("     <-", r[:100])