from scrape2 import scrape
from summarize1 import summarize

URL = "https://en.wikipedia.org/wiki/Kerala"

text = scrape(URL)
print("SCRAPED:", len(text), "chars")

s = summarize(text, "English")
print()
print("SUMMARY:")
print(s)