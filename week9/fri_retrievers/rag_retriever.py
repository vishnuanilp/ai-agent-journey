from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = Chroma(persist_directory="./chroma_fri", embedding_function=embeddings)
retriever = store.as_retriever(search_kwargs={"k": 2})

question = "can i bring my dog?"
hits = retriever.invoke(question)
context = "\n\n".join(h.page_content for h in hits)


prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer using ONLY the context. If it is not there, say you don't know."),
    ("user", "Context:\n{context}\n\nQuestion: {question}")
])

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

chain = prompt | llm | parser

answer = chain.invoke({"context": context, "question": question})

print(answer)