from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from route_nodes import retrieve_box
class RState(TypedDict, total=False):
    question: str; business: str; hits: list; error: str
r = StateGraph(RState)
r.add_node("retrieve", retrieve_box)
r.add_edge(START, "retrieve"); r.add_edge("retrieve", END)
research = r.compile()