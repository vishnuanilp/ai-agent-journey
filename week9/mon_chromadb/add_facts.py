import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()
oa = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = chromadb.PersistentClient(path="./chroma_store")
col = client.get_or_create_collection(name="clinic_facts")

def embed(texts):
    res = oa.embeddings.create(model="text-embedding-3-small", input=texts)
    return [d.embedding for d in res.data]

facts = [
    "The clinic is open from 8am to 6pm on weekdays.",
    "You must fast for 10 hours before a blood test.",
    "We accept cash, card and UPI payments.",
    "Appointments can be cancelled up to 2 hours in advance.",
]

vectors = embed(facts)

col.add(
    ids=["f1", "f2", "f3", "f4"],
    documents=facts,
    embeddings=vectors,
)

print("added. count is now:", col.count())