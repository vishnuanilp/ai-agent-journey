from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def parse(text):
    f = dict(ln.split(": ", 1) for ln in text.splitlines() if ": " in ln)
    role = text.split("for the ")[1].split(" role")[0]
    day = datetime.strptime(f["Date"], "%A %d %B %Y")
    if day.strftime("%A") != f["Date"].split()[0]: raise ValueError("WEEKDAY MISMATCH: " + f["Date"])
    hh, mm = f["Time"].split()[0].split(":")
    start = day.replace(hour=int(hh), minute=int(mm), tzinfo=ZoneInfo("Europe/Paris"))
    return "Interview - " + role, start, start + timedelta(minutes=int(f["Duration"].split()[0]))

if __name__ == "__main__":
    title, start, end = parse(open("body.txt", encoding="utf-8").read())
    print("title:", title); print("start:", start.isoformat()); print("end:  ", end.isoformat())