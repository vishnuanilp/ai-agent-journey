import json
from openai import OpenAI
from dotenv import load_dotenv
from jobtool import job_mail
from jobcard import tools

load_dotenv()
client = OpenAI()

messages = [{"role": "system", "content": "Use only the numbers the tool returns. Weekdays are on Paris time."},
            {"role": "user", "content": "Which days and which senders dominate my job hunt emails?"}]
resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
messages.append(resp.choices[0].message)
for call in resp.choices[0].message.tool_calls:
    result = job_mail(**json.loads(call.function.arguments))
    print("AI asked:", call.function.arguments, "->", result)
    messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
final = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
print("REPORT:", final.choices[0].message.content)