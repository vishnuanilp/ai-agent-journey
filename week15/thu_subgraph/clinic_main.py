from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from clinic_research import research
from clinic_analysis import analysis
class State(TypedDict, total=False):
    msg: str; hits: list; answer: str
p = StateGraph(State)
p.add_node("research", research); p.add_node("analysis", analysis)
p.add_edge(START, "research"); p.add_edge("research", "analysis"); p.add_edge("analysis", END)
app = p.compile()
for msg in ["is the doctor in tuesday?", "is there parking?", "what are your fees?"]:
    print(msg, "|", app.invoke({"msg": msg}))