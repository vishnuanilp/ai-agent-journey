from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

tools = [{"type": "function", "function": {
    "name": "sales_by_day",
    "description": "Shop sales per weekday from shop.csv. how='sum' gives money, how='count' gives number of sales.",
    "parameters": {"type": "object", "properties": {"how": {"type": "string", "enum": ["sum", "count"]}}, "required": ["how"]}}}]

question = "Which day did my shop make the most money?"
resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": question}], tools=tools)
call = resp.choices[0].message.tool_calls[0]
print("AI chose tool:", call.function.name)
print("with arguments:", call.function.arguments)