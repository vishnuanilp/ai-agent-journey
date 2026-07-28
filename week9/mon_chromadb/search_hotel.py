import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()
oa = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = chromadb.PersistentClient(path="./chroma_store")
col = client.get_or_create_collection(name="clinic_facts")

query = "can I bring my dog?"
qvec = oa.embeddings.create(model="text-embedding-3-small", input=[query]).data[0].embedding

res = col.query(query_embeddings=[qvec], n_results=2, where={"business": "hotel"})

for t, d in zip(res["documents"][0], res["distances"][0]):
    print(f"{d:.3f}  {t[:70]}...")