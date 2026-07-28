from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("products.csv")
docs = loader.load()

print("Number of Documents:", len(docs))
print("---")
print("all documents' text:", [doc.page_content for doc in docs])
print("---")
print("all documents' metadata:", [doc.metadata for doc in docs])
