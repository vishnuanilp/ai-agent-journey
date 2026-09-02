import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

html = requests.get("http://localhost:8000/evil.html").text
PAGE = BeautifulSoup(html, "html.parser").get_text()
print("--- WHAT THE MODEL WILL SEE ---")
print(PAGE)
print("--- END ---")