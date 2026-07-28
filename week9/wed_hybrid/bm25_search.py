from rank_bm25 import BM25Okapi
from chunks import chunks

tokenized = [c.lower().split() for c in chunks]
bm25 = BM25Okapi(tokenized)

query = "can i bring my dog?"
scores = bm25.get_scores(query.lower().split())

for i, s in enumerate(scores):
    print(f"[{i}] score={s:.3f}")