from langgraph.types import interrupt
from route_nodes import State

class HState(State, total=False):
    ok: str

def approve(s):
    print("  approve box START")
    reply = interrupt(f"Approve booking? -> {s['question']}")
    return {"ok": str(reply).strip().lower()}

def cancel(s): return {"answer": "OK, no booking was made."}
def route_ok(s): return "book" if s.get("ok") == "yes" else "cancel"