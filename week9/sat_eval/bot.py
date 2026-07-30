import numpy as np
from store import load_chunks, embed, client

CHUNKS = load_chunks()
VECS = np.array(embed(CHUNKS))

def retrieve(question, k):
    qv = np.array(embed([question])[0])
    sims = VECS @ qv
    top = np.argsort(sims)[::-1][:k]
    return [CHUNKS[i] for i in top]

def ask(question, k):
    context = "\n\n".join(retrieve(question, k))
    prompt = (
        "Answer the customer using ONLY the shop information below.\n"
        "If it is not there, say the information is not available.\n"
        "Answer in one short, complete sentence.\n\n"
        f"SHOP INFORMATION:\n{context}\n\nCUSTOMER: {question}"
    )
    res = client.chat.completions.create(
        model="gpt-4o-mini", temperature=0,
        messages=[{"role": "user", "content": prompt}])
    return res.choices[0].message.content.strip()

if __name__ == "__main__":
    print(ask("Is delivery free?", k=2))