from dotenv import load_dotenv
import os
from anthropic import Anthropic
import anthropic
from pymongo import MongoClient
import datetime

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["ai_agent_db"]
collection = db["agent_results"]

def save_result(topic, step, content):
    document = {
        "topic": topic,
        "step": step,
        "content": content,
        "timestamp": datetime.datetime.now()
    }
    collection.insert_one(document)

# Define tools
tools = [
    {
        "name": "calculator",
        "description": "Performs mathematical calculations. Use for any math problem.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to calculate. Example: 85000 * 0.15"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "business_scorer",
        "description": "Scores a business idea from 1-10 based on market size and competition.",
        "input_schema": {
            "type": "object",
            "properties": {
                "idea": {
                    "type": "string",
                    "description": "The business idea to score"
                },
                "market_size": {
                    "type": "string",
                    "description": "Market size: large, medium, or small"
                },
                "competition": {
                    "type": "string",
                    "description": "Competition level: low, medium, or high"
                }
            },
            "required": ["idea", "market_size", "competition"]
        }
    },
    {
        "name": "save_to_db",
        "description": "Saves important results to the database for future reference.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic being saved"
                },
                "content": {
                    "type": "string",
                    "description": "The content to save"
                }
            },
            "required": ["topic", "content"]
        }
    }
]

# Tool functions
def calculator(expression):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {e}"

def business_scorer(idea, market_size, competition):
    score = 5
    if market_size == "large":
        score += 2
    if market_size == "small":
        score -= 2
    if competition == "low":
        score += 2
    if competition == "high":
        score -= 1
    score = max(1, min(10, score))
    return f"Business Score: {score}/10"

def save_to_db(topic, content):
    save_result(topic, "tool_result", content)
    return "Saved to MongoDB!"

# Run tool based on Claude's request
def run_tool(tool_name, tool_input):
    if tool_name == "calculator":
        return calculator(tool_input["expression"])
    elif tool_name == "business_scorer":
        return business_scorer(
            tool_input["idea"],
            tool_input["market_size"],
            tool_input["competition"]
        )
    elif tool_name == "save_to_db":
        return save_to_db(
            tool_input["topic"],
            tool_input["content"]
        )
    else:
        return f"Unknown tool: {tool_name}"

# Main agent with tool use
def run_agent(user_message):
    print(f"\nUser: {user_message}")
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "tool_use":
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    print(f"\nClaude using: {tool_name}")
                    print(f"Input: {tool_input}")
                    tool_result = run_tool(tool_name, tool_input)
                    print(f"Result: {tool_result}")
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": tool_result
                        }]
                    })

        elif response.stop_reason == "end_turn":
            final_reply = response.content[0].text
            print(f"\nClaude: {final_reply}")
            return final_reply

# Test all 3 tools
print("="*50)
run_agent("What is 15% of 85000?")

print("="*50)
run_agent("Score this business idea: AI agent for tier 2 shops. Market is large and competition is medium.")

print("="*50)
run_agent("Save this to database: Topic is VocView, content is AI solutions company for Indian businesses")