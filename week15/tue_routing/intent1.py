from langgraph.graph import StateGraph, START, END
from salon_nodes import State, classify, answer, book, chat, route

g = StateGraph(State)
for name, fn in [("classify", classify), ("answer", answer), ("book", book), ("chat", chat)]:
    g.add_node(name, fn)
g.add_edge(START, "classify")
g.add_conditional_edges("classify", route, {"question": "answer", "action": "book", "chitchat": "chat"})
for name in ["answer", "book", "chat"]:
    g.add_edge(name, END)
app = g.compile()

for m in ["do you do keratin treatment?", "book me a haircut Saturday 3pm", "thanks, you're great!", "which shampoo do you use?"]:
    out = app.invoke({"msg": m})
    print(f"{m:32} -> {out['intent']:9} -> {out['answer']}")