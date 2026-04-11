from dotenv import load_dotenv
from tavily import TavilyClient
import anthropic
import os
import time

load_dotenv()


tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
client = anthropic.Anthropic()

def web_search(query):
    tavily_response = tavily.search(query)
    clean_result = ""
    for result  in tavily_response["results"][:3]: 
        clean_result +=f"""[Title: {result['title']}\n{result['content']}]\n"""
    return clean_result
    

tools =[
    {
        "name":"web_search",
        "description":"useful for when you need to answer questions about current events. input should be a search query.",
        "input_schema":{
            "type":"object",
            "properties":{
                "query":{
                    "type":"string",
                    "description":"the search query to run on the web search tool"
                }
            },
            "required":["query"]
        }
    }
]

def run_tool(tool_name,tool_input):
    if tool_name == "web_search":
        return web_search(tool_input["query"])
    else:
        return "tool not found"
    
system_prompt = """You are a research assistant that answers questions by searching the web.

For every question, follow this pattern:
1. THINK: note down your thoughts about the question and how you will answer it.
2. ACT: decide which tool to use and the input to give to that tool, then call the tool with that input.
3. OBSERVE: write down what you observed from calling the tool. If you need to call another tool, go back to step 1. If you have enough information to answer the question, go to step 4.
4. REPEAT: if you need to gather more information, repeat steps 1-3. If you have enough information to answer the question, go to step 5.
5. ANSWER: write down the final answer to the question.

Always think step by step before searching."""

user_question = input("whats your question?")

messages = [
    {"role":"user","content":user_question}

]
while True:
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,

            tools=tools,
            messages=messages
        )
    except anthropic.APIStatusError:
        print("Server busy, retrying in 5 seconds...")
        time.sleep(5)
        continue
    if response.stop_reason == "tool_use":
        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
                tool_id = block.id
                tool_result = run_tool(tool_name, tool_input)
        print(f"Searching: {tool_input['query']}")
        
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": tool_result
                }
            ]
        })
    else:
        for block in response.content:
            if hasattr(block, "text"):
                print(f"\nAnswer: {block.text}")
        break
   
    
        