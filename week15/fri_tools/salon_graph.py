from langgraph.graph import StateGraph, START, END
from salon_slots import Salon, route_slots, ask
from salon_extract import extract
from salon_approve import approve, route_reply, book, cancel
from salon_saver import saver
g = StateGraph(Salon)
for name, fn in [("extract", extract), ("ask", ask), ("approve", approve), ("book", book), ("cancel", cancel)]:
    g.add_node(name, fn)
g.add_edge(START, "extract")
g.add_conditional_edges("extract", route_slots, {"ask": "ask", "approve": "approve"})
g.add_conditional_edges("approve", route_reply, {"book": "book", "cancel": "cancel"})
for name in ("ask", "book", "cancel"):
    g.add_edge(name, END)
app = g.compile(checkpointer=saver)