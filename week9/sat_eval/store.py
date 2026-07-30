import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
EMBED_MODEL = "text-embedding-3-small"

def load_chunks(path="market_policy.txt"):
    text = open(path, encoding="utf-8").read()
    return [p.strip() for p in text.split("\n\n") if p.strip()]

def embed(texts):
    res = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in res.data]

if __name__ == "__main__":
    chunks = load_chunks()
    print(len(chunks), "chunks")
    print(len(embed(chunks)[0]), "dims")