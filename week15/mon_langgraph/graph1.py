from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    question: str
    pieces: str
    answer: str

def find_pieces(state):
    return {"pieces": "Open Tue-Sun, 12:00-22:00"}

def answer(state):
    return {"answer": "Yes, open Sunday 12:00-22:00."}

graph = StateGraph(State)
graph.add_node("find_pieces", find_pieces)
graph.add_node("answer", answer)
graph.add_edge(START, "find_pieces")
graph.add_edge("find_pieces", "answer")
graph.add_edge("answer", END)
app = graph.compile()
print("boxes :", list(app.get_graph().nodes))
print("arrows:", [(e.source, e.target) for e in app.get_graph().edges])