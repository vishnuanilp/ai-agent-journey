import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://example.com"
r = requests.get(url, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

for a in soup.find_all("a"):
    href = a.get("href")
    print("RAW      :", href)
    print("RESOLVED :", urljoin(url, href))

print("---- PROOF ----")
print(urljoin("https://shop.com/catalog/page1.html", "page2.html"))
print(urljoin("https://shop.com/catalog/page1.html", "/offers"))