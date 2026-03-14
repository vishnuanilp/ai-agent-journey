from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a startup advisor who gives very short sharp advice."},
        {"role": "user", "content": "What should I focus on in my first startup?"}
        ]
)

print(response.choices[0].message.content)