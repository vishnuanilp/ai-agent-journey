from typing import TypedDict
from langgraph.graph import StateGraph, START, END
DOCS = {"clinic_1": ("doctor", 0.6), "clinic_2": ("parking", 1.5)}   # fake distances, no API
class RState(TypedDict, total=False):
    msg: str; hits: list; raw: list
def search(s):
    return {"raw": [(k, d) for k, (word, d) in DOCS.items() if word in s["msg"]]}
def tidy(s):
    return {"hits": [(k, d) for k, d in s["raw"] if d < 1.2]}   # ALWAYS writes hits, even []
b = StateGraph(RState)
b.add_node("search", search); b.add_node("tidy", tidy)
b.add_edge(START, "search"); b.add_edge("search", "tidy"); b.add_edge("tidy", END)
research = b.compile()