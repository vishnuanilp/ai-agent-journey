from typing import TypedDict
from langgraph.types import interrupt

class State(TypedDict, total=False):
    msg: str
    ok: str
    answer: str

def approve(s):
    print("  approve box START")
    reply = interrupt(f"Book this table? -> {s['msg']}")
    return {"ok": str(reply).strip().lower()}

def book(s):   return {"answer": "Table BOOKED"}
def cancel(s): return {"answer": "Not booked"}
def route_ok(s): return "book" if s.get("ok") == "yes" else "cancel"