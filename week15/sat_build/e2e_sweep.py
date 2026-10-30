from e2e_tools import rewrite, answer_a2
from e2e_prompts import VARIANTS, CASES
for name, (doc, sys_text) in VARIANTS.items():
    good = 0
    for prev, new, want in CASES:
        for _ in range(5):
            q = rewrite(doc, sys_text, prev, new)
            a, hits = answer_a2(q)
            got = "REFUSE" if ("know" in a.lower() or "don't have" in a.lower()) else "ANSWER"
            good += got == want
            top = f"{hits[0][0]} {hits[0][2]:.3f}" if hits else "[]"
            print(f"  {name} | {'OK ' if got == want else 'BAD'} | {q} | {top} | {a[:60]}")
    print(f"{name} TOTAL {good}/15")