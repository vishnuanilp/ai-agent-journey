import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Hotel"

resp = requests.get(URL, timeout=10)
print("status:", resp.status_code)
print("html length:", len(resp.text))

soup = BeautifulSoup(resp.text, "html.parser")
text = soup.get_text()

print("text length:", len(text))
print("---- first 500 chars ----")
print(text[:500])