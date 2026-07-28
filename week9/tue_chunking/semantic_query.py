import numpy as np, chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(); oai = OpenAI()
emb = lambda xs: [d.embedding for d in oai.embeddings.create(
    model="text-embedding-3-small", input=xs).data]

text = open("hotel_policy.txt", encoding="utf-8").read()
sents = [s.strip() for s in text.replace("\n", " ").split(". ") if s.strip()]
svecs = emb(sents)

chunks, cur = [], sents[0]
for i in range(len(sents) - 1):
    if 1 - np.dot(svecs[i], svecs[i+1]) > 0.55:
        chunks.append(cur); cur = sents[i+1]
    else:
        cur += ". " + sents[i+1]
chunks.append(cur)

for i, c in enumerate(chunks):
    print("CHUNK", i, "::", repr(c[:70]))

client = chromadb.PersistentClient(path="./chroma_tue")
try: client.delete_collection("semantic")
except: pass
col = client.get_or_create_collection("semantic")
col.add(ids=[f"s{i}" for i in range(len(chunks))], documents=chunks, embeddings=emb(chunks))

res = col.query(query_embeddings=emb(["can I bring my dog?"]), n_results=2)
for doc, dist in zip(res["documents"][0], res["distances"][0]):
    print(round(dist, 3), repr(doc[:60]))