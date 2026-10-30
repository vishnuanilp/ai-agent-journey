from langgraph.types import interrupt
from room_slots import CLEAR
def approve(s):
    print("  approve box START")
    reply = interrupt(f"Approve room: check-in {s['day']}, {s['nights']} nights, {s['guests']} guests?")
    return {"ok": str(reply).strip().lower()}
def book(s):
    text = f"Booked: check-in {s['day']}, {s['nights']} nights, {s['guests']} guests. Reception will confirm by message."
    return {"answer": text, **CLEAR}
def cancel(s):
    return {"answer": "OK, no booking was made.", **CLEAR}