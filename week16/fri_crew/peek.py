import sys
from vocmem import app
cfg = {"configurable": {"thread_id": sys.argv[1]}}
v = app.get_state(cfg).values
print("QUESTION AT END OF TURN:", repr(v.get("question")))
print("--- MESSAGES ---")
for n, m in enumerate(v.get("messages", [])):
    calls = [c["args"] for c in getattr(m, "tool_calls", None) or []]
    print(n, type(m).__name__, "|", repr(m.content)[:90], "|", calls or "")
print("--- HITS ---")
for i, text, d in v.get("hits") or []:
    print(i, round(float(d), 3), "|", text[:150])