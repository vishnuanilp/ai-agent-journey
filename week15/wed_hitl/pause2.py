import sys
from saved_graph import app, DB

tid = sys.argv[1]
cfg = {"configurable": {"thread_id": tid}}
r = app.invoke({"msg": "table for 6, Sat 9pm"}, cfg)
print(tid, "PAUSED:", r["__interrupt__"][0].value)
print("saved in:", DB)