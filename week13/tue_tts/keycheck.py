import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_API_KEY")
print("OPENAI_API_KEY present:", key is not None)
print("length:", len(key) if key else 0)