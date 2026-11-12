from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import chromadb
from openai import OpenAI

HERE = Path(__file__).parent
oa = OpenAI()
col = chromadb.PersistentClient(path=str(HERE / "chroma_store")).get_collection("vocview")
CUTOFF = 1.65

def search(query, business="hotel", k=3):
    emb = oa.embeddings.create(model="text-embedding-3-small", input=[query]).data[0].embedding
    res = col.query(query_embeddings=[emb], n_results=k, where={"business": business})
    return [(t, d) for t, d in zip(res["documents"][0], res["distances"][0]) if d < CUTOFF]