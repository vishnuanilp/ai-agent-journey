import sys
from collections import Counter
from crewai.events import crewai_event_bus
from crewai.events.types.llm_events import LLMCallCompletedEvent
from crewai.events.types.tool_usage_events import ToolUsageStartedEvent
from hier2 import crew
from hotel_tool import TOOL_LOG
from counter import CALLS

ROLES, PHONE = [], []

@crewai_event_bus.on(LLMCallCompletedEvent)
def who(source, event):
    ROLES.append(getattr(event, "agent_role", None) or "?")

@crewai_event_bus.on(ToolUsageStartedEvent)
def phone(source, event):
    if "coworker" in event.tool_name:
        a = event.tool_args if isinstance(event.tool_args, dict) else {"raw": event.tool_args}
        PHONE.append((a.get("coworker", "?"), str(a.get("task") or a.get("question") or a.get("raw"))[:120]))

for q in sys.argv[1:]:
    c, s, r, p = len(CALLS), len(TOOL_LOG), len(ROLES), len(PHONE)
    out = crew.kickoff(inputs={"question": q})
    print("Q:", q)
    print("  SEARCHED:", TOOL_LOG[s:])
    for name, slip in PHONE[p:]:
        print("  PHONED:  ", name, "<-", slip.replace("\n", " "))
    for i, t in enumerate(out.tasks_output):
        print(f"  TASK{i+1}:   ", t.raw[:160].replace("\n", " "))
    print("  REPLY:   ", out.raw.replace("\n", " "))
    print("  CALLS:   ", len(CALLS) - c, "| BY ROLE", dict(Counter(ROLES[r:])))
