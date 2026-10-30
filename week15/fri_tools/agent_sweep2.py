import json, rag, search_agent as sa
CTX = "(Guest's previous message: can I bring my dog?)\nwhat about cats?"
NEW = {"role": "system", "content": "You find hotel information. Always call hotel_search. Rewrite the guest's latest message into one standalone question, using earlier messages for anything it refers to."}
def ask(rule):
    r = rag.oa.chat.completions.create(model="gpt-4o-mini", temperature=0, tools=sa.SPECS, tool_choice="required",
        messages=[rule, {"role": "user", "content": CTX}]).choices[0].message
    return json.loads(r.tool_calls[0].function.arguments)["query"]
def hits(q): return [(i, round(float(d), 3)) for i, _, d in rag.retrieve(q, "hotel")]
q = "can I bring my dog? what about cats?"
print("CODE ", f"{q!r:45}", hits(q))
for name, rule in [("OLD", sa.SYSTEM), ("NEW", NEW)]:
    for n in range(5):
        q = ask(rule); print(name, n, f"{q!r:45}", hits(q))