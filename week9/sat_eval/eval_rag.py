from testset import TESTS
from judge import judge
import rag

def run(cutoff):
    rag.CUTOFF = cutoff
    total = 0
    for t in TESTS:
        text, hits = rag.answer(t["q"], "market")
        s = judge(t["q"], t["a"], text)
        total += s["accuracy"] + s["relevance"] + s["format"]
    print(f"CUTOFF {cutoff}  TOTAL {total}/300")
    return total

for c in (1.2, 1.5, 99.0):
    run(c)