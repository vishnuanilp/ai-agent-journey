import sys
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from crew3 import crew
from hotel_tool import TOOL_LOG
from counter import CALLS

class State(TypedDict):
    question: str
    research: str
    analysis: str
    reply: str

def crew_node(state: State):
    out = crew.kickoff(inputs={"question": state["question"]})
    return {"research": out.tasks_output[0].raw,
            "analysis": out.tasks_output[1].raw,
            "reply": out.raw}

g = StateGraph(State)
g.add_node("crew", crew_node)
g.add_edge(START, "crew")
g.add_edge("crew", END)
app = g.compile()

for q in sys.argv[1:]:
    before, searched = len(CALLS), len(TOOL_LOG)
    s = app.invoke({"question": q}, {"recursion_limit": 5})
    r, a = s["research"], s["analysis"]
    print("Q:", q)
    print("  SEARCHED:", TOOL_LOG[searched:])
    print("  RESEARCH:", r[:150].replace("\n", " "))
    print("  ANALYSIS:", a.replace("\n", " "))
    print("  REPLY:   ", s["reply"].replace("\n", " "))
    print("  CALLS:   ", len(CALLS) - before, "| CTX analyst", len(r), "| writer", len(r) + len(a))
