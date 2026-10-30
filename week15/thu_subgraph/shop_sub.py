from typing import TypedDict
from langgraph.graph import StateGraph, START, END
STOCK = {"rice": 0.4, "milk": 0.7, "phone": 1.6}   # fake distances, no API
class RState(TypedDict, total=False):
    msg: str; hits: list; scratch: str
def search(s):
    found = [(w, d) for w, d in STOCK.items() if w in s["msg"]]
    return {"hits": found, "scratch": "searched"}
def tidy(s):
    return {"hits": [(w, d) for w, d in s["hits"] if d < 1.2]}
b = StateGraph(RState)
b.add_node("search", search); b.add_node("tidy", tidy)
b.add_edge(START, "search"); b.add_edge("search", "tidy"); b.add_edge("tidy", END)
research = b.compile()