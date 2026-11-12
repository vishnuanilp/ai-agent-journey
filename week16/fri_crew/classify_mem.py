import openai
from classify import classify
def classify_mem_box(s):
    guests = [m.content for m in s.get("messages", []) if m.type == "human"]
    prev = guests[-4:-1]
    text = s["question"] if not prev else "(Guest's earlier messages, oldest first: " + " | ".join(prev) + ")\n" + s["question"]
    try: return {"intent": classify(text)}
    except openai.OpenAIError as e: return {"error": f"classify: {type(e).__name__}"}
