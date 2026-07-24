import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def embed(text, model="text-embedding-3-small"):
    resp = client.embeddings.create(model=model, input=text)
    return np.array(resp.data[0].embedding)


def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

with open("facts.txt", encoding="utf-8") as f:
    facts = [line.strip() for line in f if line.strip()]

print(f"Loaded {len(facts)} facts. Embedding them once...")
fact_vectors = [embed(fact) for fact in facts]
print("Knowledge base ready.")

query = "do I need to fast before my blood test?"
query_vector = embed(query)

scored = [(cosine(query_vector, fv), fact) for fv, fact in zip(fact_vectors, facts)]
scored.sort(reverse=True)

print(f"\nQuery: {query}\n")
for score, fact in scored[:3]:
    print(f"{score:.3f}  {fact}")

print("\n--- Comparing embedding models ---")
large_vectors = [embed(f, model="text-embedding-3-large") for f in facts]
query_large = embed(query, model="text-embedding-3-large")

scored_large = [(cosine(query_large, fv), fact) for fv, fact in zip(large_vectors, facts)]
scored_large.sort(reverse=True)

print(f"\nsmall model top 3:")
for score, fact in scored[:3]:
    print(f"{score:.3f}  {fact}")

print(f"\nlarge model top 3:")
for score, fact in scored_large[:3]:
    print(f"{score:.3f}  {fact}")