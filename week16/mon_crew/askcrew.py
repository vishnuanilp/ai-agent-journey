import sys
from hotel_crew import crew
from hotel_tool import TOOL_LOG
from counter import CALLS

for q in sys.argv[1:]:
    before, searched = len(CALLS), len(TOOL_LOG)
    out = crew.kickoff(inputs={"question": q})
    print("Q:", q)
    print("  SEARCHED:", TOOL_LOG[searched:])
    print("  RESEARCH:", out.tasks_output[0].raw[:150])
    print("  REPLY:   ", out.raw)
    print("  CALLS:   ", len(CALLS) - before)