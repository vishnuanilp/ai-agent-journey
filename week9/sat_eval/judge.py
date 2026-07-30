import os, json
from dotenv import load_dotenv
from openai import OpenAI
from rubric import RUBRIC

load_dotenv()
client = OpenAI()

JUDGE_PROMPT = """You are grading a shop chatbot's answer.

""" + RUBRIC + """
QUESTION: {q}
CORRECT ANSWER: {truth}
BOT ANSWER: {answer}

Reply with ONLY this JSON, no other text:
{{"accuracy": 0, "relevance": 0, "format": 0}}
"""

def judge(q, truth, answer):
    prompt = JUDGE_PROMPT.format(q=q, truth=truth, answer=answer)
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    return json.loads(res.choices[0].message.content)

if __name__ == "__main__":
    print(judge("Is delivery free?",
                "Free on orders above 500 rupees, otherwise 40 rupees.",
                "Yes, delivery is free."))
