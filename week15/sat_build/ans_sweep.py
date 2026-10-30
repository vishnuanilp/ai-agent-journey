from vocmem import app
import rag
from ans_prompts import PROMPTS, TESTS
hits = app.get_state({"configurable": {"thread_id": "c1"}}).values["hits"]
context = "\n".join(t for _, t, _ in hits)
def ask(head, q):
    msg = f"{head}Context:\n{context}\n\nQuestion: {q}"
    r = rag.oa.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": msg}])
    return r.choices[0].message.content
for name, head in PROMPTS.items():
    score = 0
    for q, want in TESTS:
        rs = [ask(head, q) for _ in range(3)]
        bad = [r for r in rs if ("know" in r.lower()) != (want == "REFUSE")]
        score += 3 - len(bad)
        print(f"  {name} | {3 - len(bad)}/3 | {q}" + (f"  <- {bad[0][:70]}" if bad else ""))
    print(f"{name} TOTAL {score}/18")