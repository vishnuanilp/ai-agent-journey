import sqlite3
from pathlib import Path
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from route_nodes import classify_box, retrieve_box
from nodes import answer
from boxes import refuse, book, chat, error_box, route_intent, route_hits
from hitl_boxes import HState, approve, cancel, route_ok

g = StateGraph(HState)
for n, f in [("classify", classify_box), ("retrieve", retrieve_box), ("answer", answer), ("refuse", refuse),
             ("approve", approve), ("book", book), ("cancel", cancel), ("chat", chat), ("error_box", error_box)]:
    g.add_node(n, f)
g.add_edge(START, "classify")
g.add_conditional_edges("classify", route_intent,
    {"question": "retrieve", "action": "approve", "chitchat": "chat", "error": "error_box"})
g.add_conditional_edges("retrieve", route_hits, {"answer": "answer", "refuse": "refuse", "error": "error_box"})
g.add_conditional_edges("approve", route_ok, {"book": "book", "cancel": "cancel"})
for n in ["answer", "refuse", "book", "cancel", "chat", "error_box"]:
    g.add_edge(n, END)
DB = Path(__file__).parent / "vocview.db"
app = g.compile(checkpointer=SqliteSaver(sqlite3.connect(DB, check_same_thread=False)))