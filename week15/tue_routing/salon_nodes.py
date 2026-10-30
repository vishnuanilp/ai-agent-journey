from typing import TypedDict

class State(TypedDict, total=False):
    msg: str
    intent: str
    answer: str

def classify(s):
    m = s["msg"].lower()
    if "book" in m: return {"intent": "action"}
    if "hi" in m or "thanks" in m: return {"intent": "chitchat"}
    return {"intent": "question"}

def answer(s): return {"answer": "<facts box>"}
def book(s): return {"answer": "<booking box>"}
def chat(s): return {"answer": "<chat box>"}
def route(s): return s["intent"]