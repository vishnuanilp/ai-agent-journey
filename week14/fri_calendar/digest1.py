import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from auto1 import n, cal
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
now = datetime.now(ZoneInfo("Europe/Paris"))
res = cal.events().list(calendarId="primary", timeMin=now.isoformat(), timeMax=(now + timedelta(days=DAYS)).isoformat(),
                        singleEvents=True, orderBy="startTime", timeZone="Europe/Paris").execute()
lines = [f"Good morning Vishnu - {now:%A %d %B %Y} (Paris)", "", f"UPCOMING (next {DAYS} days)"]
for e in res.get("items", []):
    s, en = e["start"].get("dateTime", e["start"].get("date")), e["end"].get("dateTime", e["end"].get("date"))
    lines.append(f"  {s[:10]} {s[11:16]}-{en[11:16]}  {e.get('summary', '(no title)')}")
if len(lines) == 3: lines.append("  nothing scheduled")
lines += ["", "INTERVIEW MAIL (last 7 days)", f"  found {n['found']} | new events {n['created']} | already in calendar {n['skipped']} | could not read {n['failed']}"]
open("digest.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n"); print("\n".join(lines))