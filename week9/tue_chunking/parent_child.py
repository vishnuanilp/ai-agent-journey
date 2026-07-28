import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(); oai = OpenAI()
emb = lambda xs: [d.embedding for d in oai.embeddings.create(
    model="text-embedding-3-small", input=xs).data]

text = open("hotel_policy.txt", encoding="utf-8").read()
parents = [p.strip() for p in text.split("\n\n") if p.strip()]

children, meta = [], []
for p in parents:
    for s in [x.strip() for x in p.split(". ") if x.strip()]:
        children.append(s)
        meta.append({"parent": p})

client = chromadb.PersistentClient(path="./chroma_tue")
try: client.delete_collection("parent_child")
except: pass
col = client.get_or_create_collection("parent_child")
col.add(ids=[f"c{i}" for i in range(len(children))],
        documents=children, embeddings=emb(children), metadatas=meta)

res = col.query(query_embeddings=emb(["can I bring my dog?"]), n_results=1)
print("MATCHED CHILD :", round(res["distances"][0][0], 3), repr(res["documents"][0][0]))
print("RETURNED PARENT:", repr(res["metadatas"][0][0]["parent"][:90]))