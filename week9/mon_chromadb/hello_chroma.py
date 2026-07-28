import chromadb

client = chromadb.PersistentClient(path="./chroma_store")

collection = client.get_or_create_collection(name="clinic_facts")

print("client:", client)
print("collection:", collection.name)
print("count:", collection.count())