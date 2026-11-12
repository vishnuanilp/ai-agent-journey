import sys
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from vocbook import app
tid, text = sys.argv[1], sys.argv[2]
cfg = {"configurable": {"thread_id": tid}, "recursion_limit": 10}
paused = app.get_state(cfg).next
RESET = {"intent": None, "hits": [], "error": None, "answer": None, "ok": None}
inp = Command(resume=text) if paused else {"question": text, "business": "hotel", "messages": [HumanMessage(text)], **RESET}
app.invoke(inp, cfg)
st = app.get_state(cfg); v = st.values
print(f"{tid} | {'RESUMED' if paused else 'NEW'} | {v.get('intent')} | booking={v.get('booking')} day={v.get('day')} nights={v.get('nights')} guests={v.get('guests')} | msgs={len(v.get('messages', []))}")
print(f"{tid} | " + (f"PAUSED: {st.tasks[0].interrupts[0].value} next={st.next}" if st.next else f"{v.get('answer')}"))