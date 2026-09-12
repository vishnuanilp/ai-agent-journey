from bs4 import BeautifulSoup
from fetch1 import fetch

JUNK = ["script", "style", "nav", "header", "footer", "aside"]
MIN_LEN = 50

def scrape(url):
    r = fetch(url)
    if r is None:
        raise RuntimeError("fetch failed after retries")
    soup = BeautifulSoup(r.text, "html.parser")
    for t in soup.find_all(JUNK):
        t.decompose()
    paras = []
    for p in soup.find_all("p"):
        txt = p.get_text(separator=" ", strip=True)
        if len(txt) >= MIN_LEN:
            paras.append(txt)
    return "\n\n".join(paras)