import openai
from typing import TypedDict
import nodes
from classify import classify

class State(TypedDict, total=False):
    question: str
    business: str
    intent: str
    hits: list
    error: str
    answer: str

def classify_box(s):
    try: return {"intent": classify(s["question"])}
    except openai.OpenAIError as e: return {"error": f"classify: {type(e).__name__}"}

def retrieve_box(s):
    try: return nodes.retrieve(s)
    except openai.OpenAIError as e: return {"error": f"retrieve: {type(e).__name__}"}