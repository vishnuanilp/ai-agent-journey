import json, os
from datetime import datetime

def build(site, clip, ts, frames, fps, people):
    return {
        "site": site,
        "when": ts.strftime("%d %b %Y, %I:%M %p"),
        "what": f"{people} person(s) detected after hours",
        "lasted": f"{frames/fps:.1f}s",
        "clip": os.path.abspath(clip),
        "raised_at": datetime.now().isoformat(timespec="seconds"),
    }

def send(alert, log="alerts.jsonl"):
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(alert) + "\n")
    print(f"ALERT  {alert['site']}  {alert['when']}  {alert['what']}")
    print(f"       {alert['lasted']}  ->  {alert['clip']}")