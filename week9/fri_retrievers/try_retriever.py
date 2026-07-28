from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = Chroma(persist_directory="./chroma_fri", embedding_function=embeddings)

retriever = store.as_retriever(search_kwargs={"k": 2})

hits = retriever.invoke("can i bring my dog?")

print("how many came back:", len(hits))
for h in hits:
    print("---")
    print(h.page_content)