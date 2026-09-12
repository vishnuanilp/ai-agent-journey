import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
_client = None

def think(question, reply_lang="English"):
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a salon receptionist. Always reply in {reply_lang}, whatever language the question is in. One short sentence."},
            {"role": "user", "content": question}])
    return r.choices[0].message.content

if __name__ == "__main__":
    print(think("ขออภัยค่ะ ไม่เข้าใจคำถามของคุณ"))