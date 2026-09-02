import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PAGE = "The Grand Meridian Hotel in Kochi has 84 rooms, a rooftop pool, and airport pickup on request. Check-in is 2pm."

r = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user",
               "content": "Summarise this page in under 400 characters:\n\n" + PAGE}])
out = r.choices[0].message.content
print("chars:", len(out))
print(out)