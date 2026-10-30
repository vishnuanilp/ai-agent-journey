from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from rest_agent import agent
from rest_tools import TOOLS
from rest_saver import saver
class Chat(TypedDict):
    messages: Annotated[list, add_messages]
g = StateGraph(Chat)
g.add_node("agent", agent)
g.add_node("tools", ToolNode(TOOLS, handle_tool_errors=True))
g.add_edge(START, "agent")
g.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
g.add_edge("tools", "agent")
app = g.compile(checkpointer=saver)