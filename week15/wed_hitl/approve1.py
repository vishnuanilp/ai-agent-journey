from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver
from table_nodes import State, approve, book, cancel, route_ok

g = StateGraph(State)
g.add_node("approve", approve); g.add_node("book", book); g.add_node("cancel", cancel)
g.add_edge(START, "approve")
g.add_conditional_edges("approve", route_ok, {"book": "book", "cancel": "cancel"})
g.add_edge("book", END); g.add_edge("cancel", END)
app = g.compile(checkpointer=InMemorySaver())

for tid, msg in [("t1", "table for 4, Fri 8pm"), ("t2", "table for 20, Sat 1pm")]:
    cfg = {"configurable": {"thread_id": tid}}
    r = app.invoke({"msg": msg}, cfg)
    print(tid, "PAUSED:", r["__interrupt__"][0].value)
    reply = input("  your reply: ")
    r = app.invoke(Command(resume=reply), cfg)
    print(tid, "->", r["ok"], "|", r["answer"])