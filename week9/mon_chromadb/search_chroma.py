import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()
oa = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = chromadb.PersistentClient(path="./chroma_store")
col = client.get_or_create_collection(name="clinic_facts")

query = "should I eat before my blood test?"
qvec = oa.embeddings.create(model="text-embedding-3-small", input=[query]).data[0].embedding

res = col.query(query_embeddings=[qvec], n_results=2)

ids = res["ids"][0]
docs = res["documents"][0]
dists = res["distances"][0]

CUTOFF = 1.2
keep = [(i, t, d) for i, t, d in zip(ids, docs, dists) if d < CUTOFF]

if not keep:
    print("No relevant facts found.")
    raise SystemExit

ids, docs, dists = zip(*keep)

for text, d in zip(docs, dists):
    print(f"{d:.3f}  {text}")

context = "\n".join(docs)

prompt = f"""Answer the customer's question using ONLY the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question: {query}"""

reply = oa.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
)
print("\nANSWER:", reply.choices[0].message.content)

print("\nSOURCES:")
for i, text, d in zip(ids, docs, dists):
    print(f"  [{i}] {text}  (distance {d:.3f})")