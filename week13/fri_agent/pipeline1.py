from scrape2 import scrape
from summarize1 import summarize
from speak2 import speak

LANGS = {"hi": "Hindi", "ta": "Tamil", "ml": "Malayalam"}

def run(url, code):
    print("=== ", LANGS[code], " ===")
    text = scrape(url)
    print("SCRAPED:", len(text), "chars")
    summary = summarize(text, LANGS[code])
    print("SUMMARY:", summary)
    path = speak(summary, code, f"out_{code}.wav")
    print("AUDIO:", path)
    return path

if __name__ == "__main__":
    URL = "https://en.wikipedia.org/wiki/Kerala"
    for code in ["ml"]:
        try:
            run(URL, code)
        except Exception as e:
            print("FAILED", code, type(e).__name__, e)
        print()