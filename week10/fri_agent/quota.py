import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
try:
    r = client.models.generate_content(model="gemini-3.6-flash", contents="say ok")
    print("OK:", r.text)
except Exception as e:
    print(type(e).__name__)
    print(str(e))