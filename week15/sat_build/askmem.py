import sys
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from vocmem import app
tid, text = sys.argv[1], sys.argv[2]
cfg = {"configurable": {"thread_id": tid}, "recursion_limit": 10}
paused = app.get_state(cfg).next
RESET = {"intent": None, "hits": [], "error": None, "answer": None, "ok": None}
inp = Command(resume=text) if paused else {"question": text, "business": "hotel", "messages": [HumanMessage(text)], **RESET}
out = app.invoke(inp, cfg)
st = app.get_state(cfg); v = st.values
hits = [(i, round(float(d), 3)) for i, _, d in v.get("hits") or []]
print(f"{tid} | {'RESUMED' if paused else 'NEW'} | {v.get('intent')} | hits={hits} | error={v.get('error')} | msgs={len(v.get('messages', []))}")
print(f"{tid} | " + (f"PAUSED: {st.tasks[0].interrupts[0].value} next={st.next}" if st.next else f"{v.get('answer')}"))