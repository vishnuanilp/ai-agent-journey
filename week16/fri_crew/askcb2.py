import sys, uuid
import counter2
from langchain_core.messages import HumanMessage
from vocbook2 import app

RESET = {"intent": None, "hits": [], "error": None, "answer": None, "ok": None}
cfg = {"configurable": {"thread_id": uuid.uuid4().hex}, "recursion_limit": 10}
for q in sys.argv[1:]:
    h = counter2.HTTP.copy()
    app.invoke({"question": q, "business": "hotel", "messages": [HumanMessage(q)], **RESET}, cfg)
    v = app.get_state(cfg).values
    print("Q:", q)
    print("  INTENT:", v.get("intent"))
    print("  ANSWER:", str(v.get("answer")).replace("\n", " "))
    print("  WIRE:  ", dict(counter2.HTTP - h))
