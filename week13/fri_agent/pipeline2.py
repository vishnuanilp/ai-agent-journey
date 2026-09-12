# pipeline2.py
from ask1 import ask_url
from scrape2 import scrape
from summarize1 import summarize
from speak2 import speak

LANGS = {"en": "English", "hi": "Hindi", "ml": "Malayalam"}

def run(url, code):
    print("=== ", LANGS[code], " ===")
    text = scrape(url)
    print("SCRAPED:", len(text), "chars")
    summary = summarize(text, LANGS[code])
    print("SUMMARY:", summary)
    path = speak(summary, code, f"out_{code}.wav")
    print("AUDIO:", path)
    return path

def ask_lang():
    print("LANGUAGES:", ", ".join(f"{k}={v}" for k, v in LANGS.items()))
    code = input("Language code: ").strip().lower()
    if code not in LANGS:
        raise ValueError("unknown code: " + repr(code))
    return code

if __name__ == "__main__":
    url = ask_url()
    code = ask_lang()
    try:
        run(url, code)
    except Exception as e:
        print("FAILED", code, type(e).__name__, e)