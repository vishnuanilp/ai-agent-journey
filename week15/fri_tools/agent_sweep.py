import rag, search_agent as sa
from vocmem import app
hist = app.get_state({"configurable": {"thread_id": "c1"}}).values["messages"][:5]
NEW = {"role": "system", "content": "You find hotel information. Always call hotel_search. Rewrite the guest's latest message into one standalone question, using earlier messages for anything it refers to."}
for name, rule in [("OLD", sa.SYSTEM), ("NEW", NEW)]:
    sa.SYSTEM = rule
    for n in range(5):
        q = sa.search_agent({"messages": hist})["messages"][0].tool_calls[0]["args"]["query"]
        hits = [(i, round(float(d), 3)) for i, _, d in rag.retrieve(q, "hotel")]
        print(name, n, f"{q!r:45}", hits)