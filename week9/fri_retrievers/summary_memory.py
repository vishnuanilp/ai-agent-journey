from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationSummaryMemory

load_dotenv()

memory = ConversationSummaryMemory(llm=ChatOpenAI(model="gpt-4o-mini"))

memory.save_context({"input": "can i bring my dog?"}, {"output": "Yes, pets under 10kg, not in the dining area or pool deck."})
memory.save_context({"input": "and is there a fee?"}, {"output": "The policy does not mention a pet fee."})
memory.save_context({"input": "what time is breakfast?"}, {"output": "7am to 10am in the ground floor restaurant."})

print(memory.load_memory_variables({}))