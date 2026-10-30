from langgraph.graph import StateGraph, START, END
from nodes import State, retrieve, answer

graph = StateGraph(State)
graph.add_node("retrieve", retrieve)
graph.add_node("answer", answer)
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "answer")
graph.add_edge("answer", END)
app = graph.compile()

for q in ["can I bring my dog?", "do you sell mobile phones?"]:
    out = app.invoke({"question": q, "business": "hotel"})
    print(f"\nQ: {q}\nA: {out['answer']}")
    for i, t, d in out["hits"]:
        print(f"  [{i}] {d:.3f}  {t[:60]}...")