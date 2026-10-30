import sys
from vochitl import app

tid, q = sys.argv[1], sys.argv[2]
cfg = {"configurable": {"thread_id": tid}}
out = app.invoke({"question": q, "business": "hotel"}, cfg)
hits = [(i, round(float(d), 3)) for i, _, d in out["hits"]] if "hits" in out else "-"
if "__interrupt__" in out:
    print(f"{tid} | {out.get('intent')} | PAUSED: {out['__interrupt__'][0].value}")
    print(f"{tid} | answer={out.get('answer')} | next={app.get_state(cfg).next}")
else:
    print(f"{tid} | {out.get('intent')} | hits={hits} | error={out.get('error')} | {out['answer'][:55]}")