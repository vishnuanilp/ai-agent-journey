from typing import TypedDict

class State(TypedDict, total=False):
    msg: str
    hits: list
    answer: str

def retrieve(s): return {"hits": ["shop_1"] if "charger" in s["msg"] else []}
def answer(s): return {"answer": "Yes, we stock it."}
def refuse(s): return {"answer": "Sorry, we don't stock that."}

def route(s): return "answer" if s["hits"] else "refuse"