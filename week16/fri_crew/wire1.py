import sys
import counter2
from crew3 import crew
from counter import CALLS

for q in sys.argv[1:]:
    b, h = len(CALLS), counter2.HTTP.copy()
    out = crew.kickoff(inputs={"question": q})
    print("Q:", q)
    print("  REPLY:", out.raw.replace("\n", " "))
    print("  CALLS:", len(CALLS) - b, "| WIRE:", dict(counter2.HTTP - h))
