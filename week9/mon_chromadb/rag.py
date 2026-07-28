import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()
oa = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
col = chromadb.PersistentClient(path="./chroma_store").get_or_create_collection("vocview")

EMBED_MODEL = "text-embedding-3-small"
CUTOFF = 1.2

def embed(texts):
    res = oa.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in res.data]

def chunk(text):
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    out = []
    for i, p in enumerate(paras):
        tail = paras[i - 1].split(". ")[-1] + " " if i else ""
        out.append(tail + p)
    return out

def ingest(path, business):
    chunks = chunk(open(path, encoding="utf-8").read())
    col.add(
        ids=[f"{business}_{n}" for n in range(len(chunks))],
        documents=chunks,
        embeddings=embed(chunks),
        metadatas=[{"business": business} for _ in chunks],
    )
    return len(chunks)

def retrieve(question, business, k=3):
    res = col.query(
        query_embeddings=embed([question]),
        n_results=k,
        where={"business": business},
    )
    hits = zip(res["ids"][0], res["documents"][0], res["distances"][0])
    return [h for h in hits if h[2] < CUTOFF]

def answer(question, business):
    hits = retrieve(question, business)
    if not hits:
        return "I don't have that information.", []

    context = "\n".join(t for _, t, _ in hits)
    prompt = (
        "Answer the customer's question using ONLY the context below.\n"
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )
    reply = oa.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return reply.choices[0].message.content, hits

if __name__ == "__main__":
    print("chunks:", ingest("hotel_policy.txt", "hotel"))

    for q in ["can I bring my dog?", "do you sell mobile phones?"]:
        text, hits = answer(q, "hotel")
        print(f"\nQ: {q}\nA: {text}")
        for i, t, d in hits:
            print(f"  [{i}] {d:.3f}  {t[:60]}...")