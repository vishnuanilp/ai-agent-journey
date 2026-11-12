import sys
from crew3 import crew
from hotel_tool import TOOL_LOG
from counter import CALLS

for q in sys.argv[1:]:
    before, searched = len(CALLS), len(TOOL_LOG)
    out = crew.kickoff(inputs={"question": q})
    r, a = out.tasks_output[0].raw, out.tasks_output[1].raw
    print("Q:", q)
    print("  SEARCHED:", TOOL_LOG[searched:])
    print("  RESEARCH:", r[:150].replace("\n", " "))
    print("  ANALYSIS:", a.replace("\n", " "))
    print("  REPLY:   ", out.raw.replace("\n", " "))
    print("  CALLS:   ", len(CALLS) - before, "| CTX analyst", len(r), "| writer", len(r) + len(a))
