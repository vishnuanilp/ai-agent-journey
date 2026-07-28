import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
oai = OpenAI()
text = open("hotel_policy.txt", encoding="utf-8").read()
sents = [s.strip() for s in text.replace("\n", " ").split(". ") if s.strip()]

vecs = [d.embedding for d in oai.embeddings.create(
        model="text-embedding-3-small", input=sents).data]

for i in range(len(sents) - 1):
    gap = 1 - np.dot(vecs[i], vecs[i+1])              # distance to the NEXT sentence
    print(round(gap, 3), "|", sents[i][:50])