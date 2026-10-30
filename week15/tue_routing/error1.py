from langgraph.graph import StateGraph, START, END
from err_nodes import State, retrieve, answer, error_box, route

g = StateGraph(State)
g.add_node("retrieve", retrieve)
g.add_node("answer", answer)
g.add_node("error_box", error_box)
g.add_edge(START, "retrieve")
g.add_conditional_edges("retrieve", route, {"ok": "answer", "error": "error_box"})
g.add_edge("answer", END)
g.add_edge("error_box", END)
app = g.compile()

for m in ["phone charger", "phone charger slow"]:
    print(m, "->", app.invoke({"msg": m}))