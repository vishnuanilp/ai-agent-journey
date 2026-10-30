from langchain_core.messages import AIMessage
def remember(s):
    return {"messages": [AIMessage(s["answer"])]}