from typing import Annotated, TypedDict
from langchain_core.messages import AIMessage
from langgraph.graph.message import add_messages
class Salon(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    service: str; day: str; time: str; ok: str
FIELDS = ("service", "day", "time")
CLEAR = {k: None for k in FIELDS}
def route_slots(state):
    missing = [k for k in FIELDS if not state.get(k)]
    return "ask" if missing else "approve"
def ask(state):
    missing = [k for k in FIELDS if not state.get(k)]
    return {"messages": [AIMessage(f"Which {missing[0]} would you like?")]}