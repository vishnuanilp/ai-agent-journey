from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.memory import ConversationBufferMemory

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = Chroma(persist_directory="./chroma_fri", embedding_function=embeddings)
retriever = store.as_retriever(search_kwargs={"k": 2})

memory = ConversationBufferMemory()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a hotel assistant. Answer using ONLY the context. If it is not there, say the policy does not mention it."),
    ("user", "Conversation so far:\n{history}\n\nPolicy:\n{context}\n\nQuestion: {question}")
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

while True:
    q = input("Guest: ")
    if q.lower().strip() in ("quit", "exit"):
        break
    context = "\n\n".join(h.page_content for h in retriever.invoke(q))
    history = memory.load_memory_variables({})["history"]
    answer = chain.invoke({"history": history, "context": context, "question": q})
    memory.save_context({"input": q}, {"output": answer})
    print("Bot:", answer)
    print()