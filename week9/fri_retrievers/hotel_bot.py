from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = Chroma(persist_directory="./chroma_fri", embedding_function=embeddings)
retriever = store.as_retriever(search_kwargs={"k": 2})

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a hotel assistant. Answer using ONLY the context. If it is not there, say the policy does not mention it."),
    ("user", "Conversation so far:\n{history}\n\nPolicy:\n{context}\n\nQuestion: {question}")
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

history = []

while True:
    q = input("Guest: ")
    if q.lower() in ("quit", "exit"):
        break
    hits = retriever.invoke(q)
    context = "\n\n".join(h.page_content for h in hits)
    answer = chain.invoke({"history": "\n".join(history), "context": context, "question": q})
    history.append("Guest: " + q)
    history.append("Bot: " + answer)
    print("Bot:", answer)
    print()