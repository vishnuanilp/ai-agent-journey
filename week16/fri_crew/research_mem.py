from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from search_agent import search_agent
from search_box import search_box
class RMState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    question: str; business: str; hits: list; error: str
r = StateGraph(RMState)
r.add_node("agent", search_agent); r.add_node("search", search_box)
r.add_edge(START, "agent"); r.add_edge("agent", "search"); r.add_edge("search", END)
research = r.compile()