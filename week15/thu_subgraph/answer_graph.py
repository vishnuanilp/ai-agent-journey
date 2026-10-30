from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from nodes import answer
from boxes import refuse, error_box, route_hits
class AState(TypedDict, total=False):
    question: str; hits: list; error: str; answer: str
a = StateGraph(AState)
a.add_node("answer", answer); a.add_node("refuse", refuse); a.add_node("error_box", error_box)
a.add_conditional_edges(START, route_hits, {"answer": "answer", "refuse": "refuse", "error": "error_box"})
for n in ["answer", "refuse", "error_box"]:
    a.add_edge(n, END)
responder = a.compile()