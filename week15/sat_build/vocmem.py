import sqlite3
from pathlib import Path
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from classify_mem import classify_mem_box
from boxes import book, chat, error_box, route_intent
from hitl_boxes import approve, cancel, route_ok
from mem_state import MState
from research_mem import research
from answer_graph import responder
from remember import remember
g = StateGraph(MState)
for n, f in [("classify", classify_mem_box), ("research", research), ("respond", responder), ("approve", approve),
             ("book", book), ("cancel", cancel), ("chat", chat), ("error_box", error_box), ("remember", remember)]:
    g.add_node(n, f)
g.add_edge(START, "classify")
g.add_conditional_edges("classify", route_intent,
    {"question": "research", "action": "approve", "chitchat": "chat", "error": "error_box"})
g.add_edge("research", "respond")
g.add_conditional_edges("approve", route_ok, {"book": "book", "cancel": "cancel"})
for n in ["respond", "book", "cancel", "chat", "error_box"]:
    g.add_edge(n, "remember")
g.add_edge("remember", END)
DB = Path(__file__).parent / "vocmem.db"
app = g.compile(checkpointer=SqliteSaver(sqlite3.connect(DB, check_same_thread=False)))