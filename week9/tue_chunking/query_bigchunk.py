import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
oai = OpenAI()
text = open("hotel_policy.txt", encoding="utf-8").read()

col = chromadb.PersistentClient(path="./chroma_tue").get_or_create_collection("whole_doc")
vec = oai.embeddings.create(model="text-embedding-3-small", input=[text]).data[0].embedding
col.add(ids=["w0"], documents=[text], embeddings=[vec])

qvec = oai.embeddings.create(model="text-embedding-3-small", input=["can I bring my dog?"]).data[0].embedding
res = col.query(query_embeddings=[qvec], n_results=1)
print(round(res["distances"][0][0], 3))