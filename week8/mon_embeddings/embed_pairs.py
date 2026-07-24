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

sentences = [
    "my tooth hurts",
    "I have dental pain",
    "what are your opening hours",
    "when do you open",
    "book me a hotel room",
]

vectors = [embed(s) for s in sentences]

for i, j in combinations(range(len(sentences)), 2):
    score = cosine(vectors[i], vectors[j])
    print(f"{score:.2f}  |  {sentences[i]}  <->  {sentences[j]}")