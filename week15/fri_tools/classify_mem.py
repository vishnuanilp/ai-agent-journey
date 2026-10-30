import openai
from classify import classify
def classify_mem_box(s):
    guests = [m.content for m in s.get("messages", []) if m.type == "human"]
    text = s["question"] if len(guests) < 2 else f"(Guest's previous message: {guests[-2]})\n{s['question']}"
    try: return {"intent": classify(text)}
    except openai.OpenAIError as e: return {"error": f"classify: {type(e).__name__}"}