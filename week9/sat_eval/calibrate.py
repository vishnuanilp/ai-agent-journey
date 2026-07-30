from judge import judge
from hand_score import SAMPLES

MINE = [
    {"accuracy": 1, "relevance": 5, "format": 5},
    {"accuracy": 1, "relevance": 5, "format": 5},
    {"accuracy": 1, "relevance": 5, "format": 3},
]

for s, mine in zip(SAMPLES, MINE):
    got = judge(s["q"], s["truth"], s["answer"])
    for key in ("accuracy", "relevance", "format"):
        mark = "OK" if got[key] == mine[key] else "DIFF"
        print(mark, key, "mine", mine[key], "judge", got[key])
    print()