from langchain_core.messages import AIMessage
from langgraph.types import interrupt
from salon_slots import CLEAR
def approve(state):
    reply = interrupt(f"Approve {state['service']} on {state['day']} at {state['time']}?")
    return {"ok": str(reply).strip().lower()}
def route_reply(state):
    return "book" if state["ok"] == "yes" else "cancel"
def book(state):
    text = f"Booked: {state['service']} on {state['day']} at {state['time']}."
    return {"messages": [AIMessage(text)], **CLEAR}
def cancel(state):
    return {"messages": [AIMessage("OK, no booking was made.")], **CLEAR}