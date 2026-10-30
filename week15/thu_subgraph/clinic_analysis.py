from typing import TypedDict
from langgraph.graph import StateGraph, START, END
class AState(TypedDict, total=False):
    msg: str; hits: list; answer: str; verdict: str
def decide(s):
    return {"verdict": "ok" if s["hits"] else "none"}
def write(s):
    k, d = s["hits"][0]; return {"answer": f"Answer from {k} (distance {d})"}
def refuse(s):
    return {"answer": "I don't have that information."}
b = StateGraph(AState)
b.add_node("decide", decide); b.add_node("write", write); b.add_node("refuse", refuse)
b.add_edge(START, "decide"); b.add_edge("write", END); b.add_edge("refuse", END)
b.add_conditional_edges("decide", lambda s: s["verdict"], {"ok": "write", "none": "refuse"})
analysis = b.compile()