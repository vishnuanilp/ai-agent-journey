from langchain_classic.memory import ConversationBufferMemory

memory = ConversationBufferMemory()

memory.save_context({"input": "can i bring my dog?"}, {"output": "Yes, under 10kg."})
memory.save_context({"input": "and is there a fee?"}, {"output": "The policy does not mention a fee."})

print(memory.load_memory_variables({}))