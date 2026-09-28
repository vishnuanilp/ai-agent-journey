from datetime import datetime as dt
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

cal = build("calendar", "v3", credentials=Credentials.from_authorized_user_file("token.json"))
body = {"timeMin": "2026-10-06T00:00:00+02:00", "timeMax": "2026-10-07T00:00:00+02:00",
        "timeZone": "Europe/Paris", "items": [{"id": "primary"}]}
busy = cal.freebusy().query(body=body).execute()["calendars"]["primary"]["busy"]
print("busy blocks:", len(busy), busy)
def is_free(start, end):
    s, e = dt.fromisoformat(start), dt.fromisoformat(end)
    return not any(s < dt.fromisoformat(b["end"]) and dt.fromisoformat(b["start"]) < e for b in busy)

print("14:30-15:00 free?", is_free("2026-10-06T14:30:00+02:00", "2026-10-06T15:00:00+02:00"))
print("14:45-15:30 free?", is_free("2026-10-06T14:45:00+02:00", "2026-10-06T15:30:00+02:00"))