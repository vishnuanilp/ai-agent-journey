from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a hotel assistant. Answer briefly."),
    ("user", "Conversation so far:\n{history}\n\nQuestion: {question}")
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

history = []

def ask(question):
    text = "\n".join(history)
    answer = chain.invoke({"history": text, "question": question})
    history.append("Guest: " + question)
    history.append("Bot: " + answer)
    print("Guest:", question)
    print("Bot:", answer)
    print()

ask("can i bring my dog?")
ask("about the cancellation policy?")