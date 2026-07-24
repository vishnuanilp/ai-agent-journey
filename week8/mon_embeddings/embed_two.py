import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def embed(text):                          # turn one sentence into its vector
    reply = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(reply.data[0].embedding)   # as a numpy array, for the math

def cosine(a, b):                         # cosine similarity between two vectors
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

v1 = embed("my tooth hurts")
v2 = embed("I have dental pain")
v3 = embed("book me a hotel room")

print("tooth vs dental:", cosine(v1, v2))
print("tooth vs hotel: ", cosine(v1, v3))