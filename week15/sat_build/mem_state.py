from typing import Annotated
from langgraph.graph.message import add_messages
from hitl_boxes import HState
class MState(HState, total=False):
    messages: Annotated[list, add_messages]
    