import requests
from bs4 import BeautifulSoup

r = requests.get("https://example.com", timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

glued = soup.get_text()
clean = soup.get_text(separator=" ", strip=True)

print("GLUED :", glued)
print()
print("CLEAN :", clean)