import sys
from langgraph.types import Command
from saved_graph import app

tid, reply = sys.argv[1], sys.argv[2]
cfg = {"configurable": {"thread_id": tid}}
print(tid, "waiting at:", app.get_state(cfg).next)
r = app.invoke(Command(resume=reply), cfg)
print(tid, "->", r["ok"], "|", r["answer"])
print(tid, "next now:", app.get_state(cfg).next)