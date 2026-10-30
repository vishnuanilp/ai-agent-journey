import sqlite3
from pathlib import Path
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from route_nodes import classify_box
from boxes import book, chat, error_box, route_intent
from hitl_boxes import HState, approve, cancel, route_ok
from research_graph import research
from answer_graph import responder
g = StateGraph(HState)
for n, f in [("classify", classify_box), ("research", research), ("respond", responder), ("approve", approve),
             ("book", book), ("cancel", cancel), ("chat", chat), ("error_box", error_box)]:
    g.add_node(n, f)
g.add_edge(START, "classify")
g.add_conditional_edges("classify", route_intent,
    {"question": "research", "action": "approve", "chitchat": "chat", "error": "error_box"})
g.add_edge("research", "respond")
g.add_conditional_edges("approve", route_ok, {"book": "book", "cancel": "cancel"})
for n in ["respond", "book", "cancel", "chat", "error_box"]:
    g.add_edge(n, END)
DB = Path(__file__).parent / "vocsub.db"
app = g.compile(checkpointer=SqliteSaver(sqlite3.connect(DB, check_same_thread=False)))