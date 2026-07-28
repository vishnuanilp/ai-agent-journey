import chromadb
col = chromadb.PersistentClient(path="./chroma_tue").get_collection("semantic")
print("count:", col.count())
for d in col.get()["documents"]:
    print(repr(d[:70]))