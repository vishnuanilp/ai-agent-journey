import rag

hits = rag.retrieve("Is delivery free?", "market", k=2)
print(type(hits), len(hits))
print(hits[0])