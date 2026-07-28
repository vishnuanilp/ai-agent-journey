from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

docs = PyPDFLoader("receipt.pdf").load()
context = docs[0].page_content

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer using ONLY the context. If it's not there, say you don't know."),
    ("user", "Context: {context}\n\nQuestion: {question}")
])
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

chain = prompt | llm | parser

answer = chain.invoke({"context": context, "question": "What month is this receipt for?"})
print(answer)