import json
from openai import OpenAI
from dotenv import load_dotenv
from tool import sales_by_day
from card import tools

load_dotenv()
client = OpenAI()

messages = [{"role": "system", "content": "Use only the numbers the tool returns. Money is in Indian rupees (₹)."},
            {"role": "user", "content": "Which day did my shop make the most money?"}]
resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
call = resp.choices[0].message.tool_calls[0]
result = sales_by_day(**json.loads(call.function.arguments))
print("tool returned:", result)

messages.append(resp.choices[0].message)
messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
final = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
print("REPORT:", final.choices[0].message.content)