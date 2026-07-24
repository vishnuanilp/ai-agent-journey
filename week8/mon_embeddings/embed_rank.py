import numpy as np
from itertools import combinations
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def embed(text):
    reply = client.embeddings.create(model="text-embedding-3-small", input=text)
    return np.array(reply.data[0].embedding)

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

with open("sentences.txt", encoding="utf-8") as f:
    sentences = [line.strip() for line in f if line.strip()]

vectors = [embed(s) for s in sentences]

scores = []
for i, j in combinations(range(len(sentences)), 2):
    scores.append((cosine(vectors[i], vectors[j]), sentences[i], sentences[j]))

scores.sort(reverse=True)

for score, a, b in scores[:10]:
    print(f"{score:.2f}  |  {a}  <->  {b}")