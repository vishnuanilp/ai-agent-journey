from sentence_transformers import CrossEncoder
from chunks import chunks

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

query = "can i bring my dog?"
pairs = [(query, c) for c in chunks]
scores = reranker.predict(pairs)

for i, s in enumerate(scores):
    print(f"[{i}] rerank={s:.3f}")