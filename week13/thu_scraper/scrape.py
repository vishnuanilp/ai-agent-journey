import requests
from bs4 import BeautifulSoup

UA = "VocviewBot/0.1 (+https://vocview.com)"
JUNK = ["script", "style", "nav", "header", "footer", "aside"]

def scrape(url):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for t in soup.find_all(JUNK):
        t.decompose()
    main = soup.find("article") or soup.find("main") or soup.body
    return main.get_text(separator=" ", strip=True)

if __name__ == "__main__":
    text = scrape("https://en.wikipedia.org/wiki/Kerala")
    print("CHARS :", len(text))
    print(text[:300])