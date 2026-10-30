import sys
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from salon_graph import app
thread, text = sys.argv[1], sys.argv[2]
cfg = {"configurable": {"thread_id": thread}, "recursion_limit": 10}
paused = app.get_state(cfg).next
inp = Command(resume=text) if paused else {"messages": [HumanMessage(text)], "ok": None}
app.invoke(inp, cfg)
st = app.get_state(cfg)
v = st.values
print(f"{thread} | {'RESUMED' if paused else 'NEW'} | {v['messages'][-1].content}")
print(f"{thread} | service={v.get('service')} day={v.get('day')} time={v.get('time')}")
if st.next: print(f"{thread} | PAUSED: {st.tasks[0].interrupts[0].value} next={st.next}")