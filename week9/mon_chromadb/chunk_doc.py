text = open("hotel_policy.txt", encoding="utf-8").read()

paras = [p.strip() for p in text.split("\n\n") if p.strip()]

chunks = []
for i, p in enumerate(paras):
    if i == 0:
        chunks.append(p)
    else:
        tail = paras[i - 1].split(". ")[-1]
        chunks.append(tail + " " + p)

for c in chunks:
    print("---")
    print(c)

import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()
oa = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = chromadb.PersistentClient(path="./chroma_store")
col = client.get_or_create_collection(name="clinic_facts")

vecs = [d.embedding for d in oa.embeddings.create(
    model="text-embedding-3-small", input=chunks).data]

col.add(
    ids=[f"hotel_{n}" for n in range(len(chunks))],
    documents=chunks,
    embeddings=vecs,
    metadatas=[{"business": "hotel"} for _ in chunks],
)

print("stored:", col.count())