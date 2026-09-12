# ask1.py
def ask_url():
    raw = input("Paste a URL: ")
    url = raw.strip()
    print("GOT", len(raw), "CHARS ->", len(url), "AFTER STRIP")
    if url == "":
        raise ValueError("empty input")
    if not url.startswith(("http://", "https://")):
        raise ValueError("missing scheme: " + url[:40])
    return url


if __name__ == "__main__":
    print("URL:", ask_url())