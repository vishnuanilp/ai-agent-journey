def refuse(s): return {"answer": "I don't have that information."}
def book(s): return {"answer": "I've passed your request to reception. They'll confirm by message."}
def chat(s): return {"answer": "You're welcome! Anything else I can help with?"}
def error_box(s): return {"answer": "Sorry, something went wrong. Please call reception."}

def route_intent(s):
    if s.get("error") or s.get("intent") == "unknown": return "error"
    return s["intent"]

def route_hits(s):
    if s.get("error"): return "error"
    return "answer" if s["hits"] else "refuse"