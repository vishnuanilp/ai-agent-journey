import sys, os, uuid
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"D:\vocview\ai-agent-journey\week17\mon_redis")
from langchain_core.messages import HumanMessage
from vocbook3 import app          # vocbook3 sets fri_crew path + chdir
sys.path.insert(0, HERE)
import counter3

RESET = {"intent": None, "hits": [], "error": None, "answer": None, "ok": None}
cfg = {"configurable": {"thread_id": uuid.uuid4().hex}, "recursion_limit": 10}
for q in sys.argv[1:]:
    h = counter3.HTTP.copy()
    n = len(counter3.ROWS)
    app.invoke({"question": q, "business": "hotel", "messages": [HumanMessage(q)], **RESET}, cfg)
    v = app.get_state(cfg).values
    rows = counter3.ROWS[n:]
    priced = [r for r in rows if r["cost"] is not None]
    cost = sum(r["cost"] for r in priced)
    print("Q:", q)
    print("  INTENT:", v.get("intent"))
    print("  ANSWER:", str(v.get("answer")).replace("\n", " "))
    print("  WIRE:  ", dict(counter3.HTTP - h))
    for r in rows:
        print("  ROW:   ", r["path"], r["model"], r["tin"], r["tout"], r["cost"])
    print(f"  COST:   ${cost:.6f}  tokens in {sum(r['tin'] for r in rows)}"
          f" out {sum(r['tout'] for r in rows)}  priced {len(priced)}/{len(rows)}")
