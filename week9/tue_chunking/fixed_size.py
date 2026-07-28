import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
oai = OpenAI()
text = open("hotel_policy.txt", encoding="utf-8").read()
chunks = [text[i:i+120] for i in range(0, len(text), 120)]   # blind 120-char cuts

vecs = [d.embedding for d in oai.embeddings.create(model="text-embedding-3-small", input=chunks).data]
col = chromadb.PersistentClient(path="./chroma_tue").get_or_create_collection("fixed")
col.add(ids=[f"f{i}" for i in range(len(chunks))], documents=chunks, embeddings=vecs)

qvec = oai.embeddings.create(model="text-embedding-3-small", input=["can I bring my dog?"]).data[0].embedding
res = col.query(query_embeddings=[qvec], n_results=2)
for doc, dist in zip(res["documents"][0], res["distances"][0]):
    print(round(dist, 3), repr(doc[:60]))