import requests
from bs4 import BeautifulSoup

r = requests.get("https://example.com", timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

paras = soup.find_all("p")

print("HOW MANY :", len(paras))
print("TYPE     :", type(paras))
for p in paras:
    print("PARA :", p.get_text(separator=" ", strip=True))