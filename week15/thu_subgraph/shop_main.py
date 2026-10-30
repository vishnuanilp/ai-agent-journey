from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from shop_sub import research
class State(TypedDict, total=False):
    msg: str; intent: str; hits: list; answer: str
def classify(s): return {"intent": "question"}            # stub, no API
def answer(s): return {"answer": f"In stock: {s['hits']}" if s["hits"] else "Sorry, not in stock."}
p = StateGraph(State)
p.add_node("classify", classify); p.add_node("research", research); p.add_node("answer", answer)
p.add_edge(START, "classify"); p.add_edge("classify", "research")
p.add_edge("research", "answer"); p.add_edge("answer", END)
app = p.compile()
for msg in ["do you have rice?", "any phone?"]:
    print(msg, "|", app.invoke({"msg": msg}))