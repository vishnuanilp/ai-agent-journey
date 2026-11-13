import os, sys, sqlite3
from pathlib import Path
HERE = Path(__file__).resolve().parent
FRI = HERE.parents[1] / "week16" / "fri_crew"
sys.path.insert(0, str(FRI))
os.chdir(FRI)
import redis
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from classify_mem import classify_mem_box
from boxes import chat, error_box, route_intent
from hitl_boxes import route_ok
from room_slots import BState, route_start, route_extract, ask
from room_extract import extract
from room_book import approve, book, cancel
from remember import remember
from hotel_crew import find
from crew3 import crew

find.description = ("Guest asks: {question}\n"
    "Search the hotel documents and copy the policy text about this topic, "
    "even if it says no or sets a limit. "
    "Write NOT FOUND only if no returned text is about the topic.")
find._original_description = None

R = redis.Redis(decode_responses=True)
TTL = 3600

def cache_key(s):
    q = " ".join(str(s["question"]).lower().split())
    return f"vocview:{s.get('business')}:{q}"

def crew_box(s):
    k = cache_key(s)
    try:
        hit = R.get(k)
    except redis.RedisError:
        hit = None
    if hit is not None:
        print("  CACHE: HIT ", k)
        return {"answer": hit}
    print("  CACHE: MISS", k)
    out = crew.kickoff(inputs={"question": s["question"]})
    try:
        R.set(k, out.raw, ex=TTL)
    except redis.RedisError:
        pass
    return {"answer": out.raw}

g = StateGraph(BState)
for n, f in [("classify", classify_mem_box), ("crew", crew_box), ("extract", extract), ("ask", ask),
             ("approve", approve), ("book", book), ("cancel", cancel), ("chat", chat), ("error_box", error_box), ("remember", remember)]:
    g.add_node(n, f)
g.add_conditional_edges(START, route_start, {"extract": "extract", "classify": "classify"})
g.add_conditional_edges("classify", route_intent,
    {"question": "crew", "action": "extract", "chitchat": "chat", "error": "error_box"})
g.add_conditional_edges("extract", route_extract, {"classify": "classify", "ask": "ask", "approve":"approve", "cancel": "cancel"})
g.add_conditional_edges("approve", route_ok, {"book": "book", "cancel": "cancel"})
for n in ["crew", "ask", "book", "cancel", "chat", "error_box"]:
    g.add_edge(n, "remember")
g.add_edge("remember", END)
DB = HERE / "vocbook3.db"
app = g.compile(checkpointer=SqliteSaver(sqlite3.connect(DB, check_same_thread=False)))
