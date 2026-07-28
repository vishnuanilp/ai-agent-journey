from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

docs = TextLoader("hotel_policy.txt", encoding="utf-8").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40).split_documents(docs)

print("chunks:", len(chunks))

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_fri")

print("stored:", store._collection.count())