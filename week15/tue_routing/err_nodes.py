from typing import TypedDict

class State(TypedDict, total=False):
    msg: str
    hits: list
    error: str
    answer: str

def search(msg):
    if "slow" in msg: raise TimeoutError("search timed out")
    return ["shop_1"]

def retrieve(s):
    try: return {"hits": search(s["msg"])}
    except TimeoutError as e: return {"error": f"retrieve: {e}"}

def answer(s): return {"answer": f"Yes, we stock it ({s['hits'][0]})."}
def error_box(s): return {"answer": "Sorry, I couldn't check right now. Please call the shop."}
def route(s): return "error" if s.get("error") else "ok"