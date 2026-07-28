import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
oai = OpenAI()
q = "can I bring my dog?"
qvec = oai.embeddings.create(
    model="text-embedding-3-small", input=[q]).data[0].embedding

col = chromadb.PersistentClient(path="./chroma_tue").get_collection("recursive")
res = col.query(query_embeddings=[qvec], n_results=2)

for doc, dist in zip(res["documents"][0], res["distances"][0]):
    print(round(dist, 3), repr(doc[:60]))