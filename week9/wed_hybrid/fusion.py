import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from rank_bm25 import BM25Okapi
from chunks import chunks

load_dotenv()
client = OpenAI()

def embed(texts):
    r = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [d.embedding for d in r.data]

chroma = chromadb.PersistentClient(path="./chroma_wed")
try:
    chroma.delete_collection("vocview")
except Exception:
    pass
col = chroma.get_or_create_collection("vocview")

ids = [f"c{i}" for i in range(len(chunks))]
col.add(ids=ids, documents=chunks, embeddings=embed(chunks))

query = "can i bring my dog?"

vec = col.query(query_embeddings=embed([query]), n_results=5)
vec_ranking = vec["ids"][0]

bm25 = BM25Okapi([c.lower().split() for c in chunks])
scores = bm25.get_scores(query.lower().split())
key_ranking = [f"c{i}" for i in sorted(range(len(chunks)), key=lambda i: -scores[i])]

def rrf(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, cid in enumerate(ranking):
            scores[cid] = scores.get(cid, 0) + 1 / (k + rank)
    return sorted(scores, key=lambda cid: -scores[cid])

fused = rrf([vec_ranking, key_ranking])
print("vector: ", vec_ranking)
print("keyword:", key_ranking)
print("fused:  ", fused)

from sentence_transformers import CrossEncoder

TOP_K = 3
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

candidates = fused[:TOP_K]
cand_text = [chunks[int(cid[1:])] for cid in candidates]

pairs = [(query, t) for t in cand_text]
final = reranker.predict(pairs)

order = sorted(range(len(candidates)), key=lambda i: -final[i])
print("\nreranked top-k:")
for i in order:
    print(f"  {candidates[i]} score={final[i]:.3f}")