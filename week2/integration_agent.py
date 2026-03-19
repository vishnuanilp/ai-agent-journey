from dotenv import load_dotenv
import os
from anthropic import Anthropic
import anthropic
from pymongo import MongoClient
import datetime
import time

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["ai_agent_db"]
collection = db["business_research"]

print("Integration Agent ready!")
# Tool definitions
tools = [
    {
        "name": "business_scorer",
        "description": "Scores a business idea from 1-10 based on market size and competition.",
        "input_schema": {
            "type": "object",
            "properties": {
                "idea": {"type": "string", "description": "The business idea"},
                "market_size": {"type": "string", "description": "large, medium, or small"},
                "competition": {"type": "string", "description": "low, medium, or high"}
            },
            "required": ["idea", "market_size", "competition"]
        }
    },
    {
        "name": "save_research",
        "description": "Saves research results to MongoDB database.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The research topic"},
                "findings": {"type": "string", "description": "The research findings to save"}
            },
            "required": ["topic", "findings"]
        }
    }
]

def business_scorer(idea, market_size, competition):
    score = 5
    if market_size == "large": score += 2
    if market_size == "small": score -= 2
    if competition == "low": score += 2
    if competition == "high": score -= 1
    score = max(1, min(10, score))
    return f"Business Score: {score}/10"

def save_research(topic, findings):
    document = {
        "topic": topic,
        "findings": findings,
        "timestamp": datetime.datetime.now()
    }
    collection.insert_one(document)
    return "Research saved to MongoDB!"

def run_tool(tool_name, tool_input):
    if tool_name == "business_scorer":
        return business_scorer(
            tool_input["idea"],
            tool_input["market_size"],
            tool_input["competition"]
        )
    elif tool_name == "save_research":
        return save_research(
            tool_input["topic"],
            tool_input["findings"]
        )
    return f"Unknown tool: {tool_name}"

print("Tools ready!")

# Main research agent
def run_research_agent(topic):
    print(f"\n{'='*50}")
    print(f"Researching: {topic}")
    print(f"{'='*50}")

    # Step 1 - Research with XML tags
    research_prompt = f"""
<task>Research this business topic deeply</task>
<topic>{topic}</topic>
<rules>
- Find 5 key market insights
- Identify target customers
- Find main competitors
- Estimate market size: large medium or small
- Estimate competition: low medium or high
- Keep each point concise
</rules>
<format>
Market Insights:
Target Customers:
Main Competitors:
Market Size: large/medium/small
Competition: low/medium/high
</format>
"""
    print("\n🔍 Step 1: Researching...")
    try:
        research_response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=800,
            messages=[{"role": "user", "content": research_prompt}]
        )
        research = research_response.content[0].text
        print("✅ Research complete!")
        print(research)

    except Exception as e:
        print(f"❌ Research failed: {e}")
        return

    # Step 2 - Score and save using tools
    print("\n🔧 Step 2: Scoring and saving...")
    score_prompt = f"""
<task>Score this business idea and save the research</task>
<topic>{topic}</topic>
<research>{research}</research>
<instructions>
1. Use business_scorer tool to score the idea
   Extract market_size and competition from research
2. Use save_research tool to save findings to database
3. Give final recommendation
</instructions>
"""
    messages = [{"role": "user", "content": score_prompt}]

    while True:
        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1000,
                tools=tools,
                messages=messages
            )

            if response.stop_reason == "tool_use":
                # Add Claude's response to messages first
                messages.append({"role": "assistant", "content": response.content})
                
                # Collect ALL tool results together
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"Claude using: {block.name}")
                        tool_result = run_tool(block.name, block.input)
                        print(f"Result: {tool_result}")
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": tool_result
                        })
                
                # Send ALL results together in one message
                messages.append({
                    "role": "user",
                    "content": tool_results
                })

            elif response.stop_reason == "end_turn":
                final = response.content[0].text
                print(f"\n{'='*50}")
                print("FINAL RECOMMENDATION:")
                print(f"{'='*50}")
                print(final)
                return

        except anthropic.RateLimitError:
            print("Rate limited! Waiting 2 seconds...")
            time.sleep(2)

        except Exception as e:
            print(f"❌ Error: {e}")
            return

# Run the agent!
run_research_agent("AI agent for tier 2 shop owners in India")