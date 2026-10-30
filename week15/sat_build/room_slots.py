from mem_state import MState
class BState(MState, total=False):
    day: str; nights: str; guests: str; booking: str; found: int; stop: bool
FIELDS = ("day", "nights", "guests")
CLEAR = {k: None for k in FIELDS + ("booking", "stop")}
QUESTIONS = {"day": "Which day would you like to check in?", "nights": "How many nights?", "guests": "How many guests?"}
def route_start(s): return "extract" if s.get("booking") == "open" else "classify"
def route_extract(s):
    if s.get("stop"): return "cancel"
    if not s.get("found") and not s.get("intent"): return "classify"
    return "ask" if [k for k in FIELDS if not s.get(k)] else "approve"
def ask(s):
    missing = [k for k in FIELDS if not s.get(k)]
    return {"answer": QUESTIONS[missing[0]]}
