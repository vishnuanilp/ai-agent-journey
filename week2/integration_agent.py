
import anthropic
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
client = anthropic.Anthropic() 
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["week2_agents"]
collection = db["tool_history"]
 
def save_to_mongodb(step,topic,content):
    doc = {
        "step": step,
        "topic": topic,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    collection.insert_one(doc)

def calculate(expression):
    """Safely evaluate a simple math expression."""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error in calculation" 
    
def business_scorer(idea,market_size,competition):
    """Scores a business idea from 1-10"""
    try:
        score = 5
        if market_size == "large":
            score += 2
        if market_size == "small":
            score -= 2
        if competition == "low":
            score += 2
        if competition == "high":
            score -= 1
        score = max(1,min(10,score))
        return f"Business idea score: {idea}.score : {score}/10"
        
    except:
        return "Error in scoring"
def save_to_notes(topic,content):
    """Saves content to a notes collection in MongoDB."""
    try:
     save_to_mongodb("user_note",topic,content)
     return "saved database"
    except:
        return "Error in saving to notes"
    
tools = [
    {
        "name": "calculate",
        "description": "Performs basic math operations. Use this when the user asks to calculate something.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "business_scorer",
        "description": "Scores a business idea from 1-10. Use this when the user wants feedback on a business idea.",
        "input_schema": {
            "type": "object",
            "properties": {
                "idea": {
                    "type": "string",
                    "description": "The business idea to score"
                },
                "market_size": {
                    "type": "string",
                    "description": "The market size (small, medium, large)"
                },
                "competition": {
                    "type": "string",
                    "description": "The level of competition (low, medium, high)"
                }
            },
            "required": ["idea", "market_size", "competition"]
        }
    },
    {
        "name": "save_to_notes",
        "description": "Saves content to a notes collection in MongoDB. Use this when the user wants to save something for later reference.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic of the note"
                },
                "content": {
                    "type": "string",
                    "description": "The content to save in the note"
                }
            },
            "required": ["topic", "content"]
        }
    }
]

def run_tool(tool_name, tool_input):
    if tool_name =="calculate":
        return calculate(tool_input["expression"])
    elif tool_name == "business_scorer":
        return business_scorer(tool_input["idea"], tool_input["market_size"], tool_input["competition"])
    elif tool_name == "save_to_notes":
        return save_to_notes(tool_input["topic"], tool_input["content"])
    
def chat_with_agent(user_message):
    print(f"User: {user_message}")
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            final_text = response.content[0].text
            print(f"Agent: {final_text}")
            return  final_text  
        if response.stop_reason == "tool_use":
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_id = block.id
                    result = run_tool(tool_name, tool_input)
                    save_to_mongodb("tool_use",tool_name,result)
                    print(f"Tool {tool_name} returned: {result}")
                    print(f"result:{result}")

                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({
                                "role": "user",
                                "content": [{
                                    "type": "tool_result",
                                    "tool_use_id": tool_id,
                                    "content": result
                                }]
                            })
print("=== Tool Use Agent ===")
print("Type 'quit' to exit\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    chat_with_agent(user_input) 
