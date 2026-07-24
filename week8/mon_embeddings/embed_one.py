import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()                        # read .env, so OPENAI_API_KEY is available
client = OpenAI()                    # build the client (it reads the key for us)

response = client.embeddings.create(
    model="text-embedding-3-small",  # which embedding model to use
    input="my tooth hurts"           # the sentence we want as numbers
)

vector = response.data[0].embedding  # pull the list of numbers out of the reply
print(len(vector))                   # how many numbers? = the dimensions
print(vector[:5])                    # peek at just the first five