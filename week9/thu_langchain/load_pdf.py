from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("receipt.pdf")
docs = loader.load()

print("Number of Documents:", len(docs))
print("---")
print("Text of first page:", docs[0].page_content)
print("---")
print("Where it came from:", docs[0].metadata)