import sys
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from rest_graph import app

thread, text = sys.argv[1], sys.argv[2]
cfg = {"configurable": {"thread_id": thread}, "recursion_limit": 10}
before = len(app.get_state(cfg).values.get("messages", []))
out = app.invoke({"messages": [HumanMessage(text)]}, cfg)
for m in out["messages"][before:]:
    if isinstance(m, AIMessage) and m.tool_calls:
        for c in m.tool_calls: print(f"  CALL   {c['name']}({c['args']})")
    if isinstance(m, ToolMessage): print(f"  RESULT {m.content}")
print(f"{thread} | {out['messages'][-1].content}")
print(f"{thread} | messages in notebook: {len(out['messages'])}")