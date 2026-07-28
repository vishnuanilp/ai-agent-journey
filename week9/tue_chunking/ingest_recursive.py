import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from recursive_split import split_recursive

load_dotenv()
oai = OpenAI()
text = open("hotel_policy.txt", encoding="utf-8").read()
chunks = split_recursive(text, ["\n\n", "\n", ". "], 300)

vecs = [d.embedding for d in oai.embeddings.create(
        model="text-embedding-3-small", input=chunks).data]

client = chromadb.PersistentClient(path="./chroma_tue")
col = client.get_or_create_collection("recursive")
col.add(ids=[f"r{i}" for i in range(len(chunks))],
        documents=chunks, embeddings=vecs)
print("stored:", col.count())