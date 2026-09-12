from batch1 import scrape_many

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://this-domain-does-not-exist-vocview.com",
    "https://en.wikipedia.org/wiki/Kerala",
]

good, bad = scrape_many(urls)

print()
for url, text in good:
    print("OK   ", len(text), "chars", url)
for url, reason in bad:
    print("FAIL ", reason, url)