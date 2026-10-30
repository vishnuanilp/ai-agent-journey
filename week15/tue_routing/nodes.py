from typing import TypedDict
import rag

class State(TypedDict):
    question: str
    business: str
    hits: list
    answer: str

def retrieve(state):
    return {"hits": rag.retrieve(state["question"], state["business"])}

def answer(state):
    if not state["hits"]:
        return {"answer": "I don't have that information."}
    context = "\n".join(t for _, t, _ in state["hits"])
    prompt = (
        "Answer the customer's question using ONLY the context below.\n"
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {state['question']}"
    )
    reply = rag.oa.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    return {"answer": reply.choices[0].message.content}