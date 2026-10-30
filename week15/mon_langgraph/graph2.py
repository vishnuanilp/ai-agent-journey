from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    question: str
    answer: str

def process(state):
    return {"answer": "Yes, open Sunday 12:00-22:00."}

graph = StateGraph(State)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
app = graph.compile()
print(app.invoke({"question": "Are you open on Sunday?"}))