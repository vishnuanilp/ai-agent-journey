import openai
from langchain_core.messages import ToolMessage
import rag
def search_box(s):
    call = s["messages"][-1].tool_calls[0]
    query = call["args"]["query"]
    try:
        hits = rag.retrieve(query, s["business"])
    except openai.OpenAIError as e:
        return {"hits": [], "error": f"search: {type(e).__name__}", "question": query,
                "messages": [ToolMessage("search failed", tool_call_id=call["id"])]}
    ids = [(i, round(float(d), 3)) for i, _, d in hits]
    return {"hits": hits, "error": None, "question": query, "messages": [ToolMessage(str(ids), tool_call_id=call["id"])]}