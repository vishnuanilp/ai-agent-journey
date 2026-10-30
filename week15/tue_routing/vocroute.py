from langgraph.graph import StateGraph, START, END
from route_nodes import State, classify_box, retrieve_box
from nodes import answer
from boxes import refuse, book, chat, error_box, route_intent, route_hits

g = StateGraph(State)
for n, f in [("classify", classify_box), ("retrieve", retrieve_box), ("answer", answer),
             ("refuse", refuse), ("book", book), ("chat", chat), ("error_box", error_box)]:
    g.add_node(n, f)
g.add_edge(START, "classify")
g.add_conditional_edges("classify", route_intent,
    {"question": "retrieve", "action": "book", "chitchat": "chat", "error": "error_box"})
g.add_conditional_edges("retrieve", route_hits, {"answer": "answer", "refuse": "refuse", "error": "error_box"})
for n in ["answer", "refuse", "book", "chat", "error_box"]:
    g.add_edge(n, END)
app = g.compile()

for q in ["can I bring my dog?", "do you sell mobile phones?", "which room has a sea view?",
          "book me a room for Saturday", "thanks, you're great!"]:
    out = app.invoke({"question": q, "business": "hotel"})
    hits = [(i, round(d, 3)) for i, _, d in out.get("hits", [])] if "hits" in out else "-"
    print(f"{q:28} | {out.get('intent')} | hits={hits} | {out['answer'][:55]}")