import requests
from urllib.robotparser import RobotFileParser

UA = "VocviewBot/0.1 (+https://vocview.com; contact v.vocview@gmail.com)"
r = requests.get("https://en.wikipedia.org/robots.txt",
                 headers={"User-Agent": UA}, timeout=10)
print("STATUS :", r.status_code, "| LENGTH :", len(r.text))

if r.status_code != 200:
    print("NO RULES FETCHED — DO NOT TRUST ANY ANSWER")
else:
    rp = RobotFileParser()
    rp.parse(r.text.splitlines())
    print("ALLOW :", rp.can_fetch(UA, "https://en.wikipedia.org/wiki/Kerala"))
    print("EDIT  :", rp.can_fetch(UA, "https://en.wikipedia.org/w/index.php?action=edit"))