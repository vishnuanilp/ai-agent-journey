import sqlite3
from pathlib import Path
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from table_nodes import State, approve, book, cancel, route_ok

DB = Path(__file__).parent / "bookings.db"
g = StateGraph(State)
g.add_node("approve", approve); g.add_node("book", book); g.add_node("cancel", cancel)
g.add_edge(START, "approve")
g.add_conditional_edges("approve", route_ok, {"book": "book", "cancel": "cancel"})
g.add_edge("book", END); g.add_edge("cancel", END)
conn = sqlite3.connect(DB, check_same_thread=False)
app = g.compile(checkpointer=SqliteSaver(conn))