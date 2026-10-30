from langgraph.graph import StateGraph, START, END
from shop_nodes import State, retrieve, answer, refuse, route

g = StateGraph(State)
g.add_node("retrieve", retrieve)
g.add_node("answer", answer)
g.add_node("refuse", refuse)
g.add_edge(START, "retrieve")
g.add_conditional_edges("retrieve", route, {"answer": "answer", "refuse": "refuse"})
g.add_edge("answer", END)
g.add_edge("refuse", END)
app = g.compile()

for m in ["phone charger", "lipstick"]:
    print(m, "->", app.invoke({"msg": m}))