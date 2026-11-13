import sys, uuid, csv, datetime
from collections import defaultdict
from pathlib import Path
from langchain_core.messages import HumanMessage
from vocbook4 import app          # vocbook4 sets fri_crew path + chdir
import counter3

HARD_MISS = 0.003853   # measured mean of 3 hard MISS runs (cat), 12 Nov
LOG = Path(__file__).resolve().parent / "spend_log.csv"
BIZ = "hotel"
QS = ["do you have a gym?", "do you have a gym?",
      "I'm bringing my 8 kg cat. Can she stay with me, and can she come to dinner and then to the pool?",
      "I'm bringing my 8 kg cat. Can she stay with me, and can she come to dinner and then to the pool?",
      "are pets allowed?"]

RESET = {"intent": None, "hits": [], "error": None, "answer": None, "ok": None}
cfg = {"configurable": {"thread_id": uuid.uuid4().hex}, "recursion_limit": 10}
day = datetime.date.today().isoformat()
per_q, per_model, misses, hit_cost = [], defaultdict(float), 0, 0.0
with LOG.open("a", newline="") as f:
    w = csv.writer(f)
    for q in QS:
        n = len(counter3.ROWS)
        app.invoke({"question": q, "business": BIZ, "messages": [HumanMessage(q)], **RESET}, cfg)
        rows = counter3.ROWS[n:]
        cost = sum(r["cost"] or 0 for r in rows)
        miss = len(rows) > 1
        misses += miss
        hit_cost += 0 if miss else cost
        per_q.append((q[:40], "MISS" if miss else "HIT", cost))
        for r in rows:
            per_model[r["model"].split("-20")[0]] += r["cost"] or 0
            w.writerow([day, BIZ, q, r["path"], r["model"], r["tin"], r["tout"], r["cost"]])
total = sum(c for _, _, c in per_q)
for q, kind, c in per_q:
    print(f"PERQ:  {kind:4} ${c:.6f}  {q}")
for m, c in per_model.items():
    print(f"MODEL: ${c:.6f}  {m}")
print(f"BIZ:   {BIZ} ${total:.6f}   DAY: {day} ${total:.6f}")
print(f"ALLSONNET: ${hit_cost + misses * HARD_MISS:.6f} (estimate)  ROUTED: ${total:.6f}")
