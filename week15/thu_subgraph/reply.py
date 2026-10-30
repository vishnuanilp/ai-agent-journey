import sys
from langgraph.types import Command
from vochitl import app

tid, reply = sys.argv[1], sys.argv[2]
cfg = {"configurable": {"thread_id": tid}}
print(tid, "waiting at:", app.get_state(cfg).next)
out = app.invoke(Command(resume=reply), cfg)
print(f"{tid} | {out.get('intent')} | ok={out.get('ok')} | {out['answer'][:55]}")
print(tid, "next now:", app.get_state(cfg).next)