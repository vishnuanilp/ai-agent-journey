import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    answer: str
    messages: Annotated[list, operator.add]

def draft(state):
    return {"answer": "Open till 23:00", "messages": ["draft"]}

def correct(state):
    return {"answer": "Open till 22:00", "messages": ["correct"]}

graph = StateGraph(State)
graph.add_node("draft", draft)
graph.add_node("correct", correct)
graph.add_edge(START, "draft")
graph.add_edge("draft", "correct")
graph.add_edge("correct", END)
print(graph.compile().invoke({"answer": "", "messages": ["customer: open Sunday?"]}))