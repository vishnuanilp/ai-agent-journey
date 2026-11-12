from par_tools import rewrite_all
from e2e_tools import answer_a2
from par_prompts import VARIANTS, CASES, SYS
for name, (doc, parallel) in VARIANTS.items():
    good = multi = 0
    for prev, new, want in CASES:
        for _ in range(3):
            qs = rewrite_all(doc, SYS, prev, new, parallel)
            a, hits = answer_a2(qs[0])
            got = "REFUSE" if ("know" in a.lower() or "don't have" in a.lower()) else "ANSWER"
            good += got == want
            multi += len(qs) > 1
            print(f"  {name} | {'OK ' if got == want else 'BAD'} | {new} -> {qs} | {a[:50]}")
    print(f"{name} TOTAL {good}/15 | multi-call runs {multi}/15")