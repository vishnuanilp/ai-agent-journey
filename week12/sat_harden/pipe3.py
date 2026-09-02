import os, time, requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
from urlcheck import check_url
from sanitize import sanitize
from limiter import allow, record
from speak2 import deliver

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
USER = "hotel_desk"
URL = "https://en.wikipedia.org/wiki/Hotel"
HEADERS = {"User-Agent": "VocviewListenToTheWeb/0.1 (vishnu@example.com)"}

t0 = time.time()
if not allow(USER, "ratelimit"):
    raise SystemExit("REFUSED: daily limit")

ok, why = check_url(URL)
record(USER, "urlcheck", "OK" if ok else "REFUSED: " + why)
if not ok:
    raise SystemExit("REFUSED at urlcheck")

t = time.time()
resp = requests.get(URL, timeout=10, headers=HEADERS)
record(USER, "fetch", "OK " + str(resp.status_code), int((time.time() - t) * 1000))
if resp.status_code != 200:
    raise SystemExit("REFUSED: " + str(resp.status_code))

raw = BeautifulSoup(resp.text, "html.parser").select_one("#mw-content-text").get_text(" ", strip=True)
clean, log = sanitize(raw)
record(USER, "sanitize", "truncated " + str(log["truncated"]))
if log["regex_hit"]:
    record(USER, "sanitize", "REFUSED: injection pattern")
    raise SystemExit("REFUSED at sanitize")

t = time.time()
r = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user",
               "content": "Summarise this page in under 400 characters:\n\n" + clean}])
summary = r.choices[0].message.content
record(USER, "model", "OK " + str(len(summary)) + " chars", int((time.time() - t) * 1000))

verdict = deliver(summary)
record(USER, "speak", verdict)
record(USER, "pipeline", "COMPLETE " + verdict, int((time.time() - t0) * 1000))