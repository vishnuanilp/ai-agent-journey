import os, sys
from dotenv import load_dotenv
from google import genai

print("PYTHON:", sys.executable)
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

while True:
    q = input("\nyou: ")
    if q.strip().lower() == "quit":
        break
    resp = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=q)
    print("agent:", resp.text)