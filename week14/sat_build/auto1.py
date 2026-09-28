from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from gmailbody import body
from parse1 import parse
creds = Credentials.from_authorized_user_file("token.json")
gm, cal = build("gmail", "v1", credentials=creds), build("calendar", "v3", credentials=creds)
ids = [m["id"] for m in gm.users().messages().list(userId="me", q="subject:interview newer_than:7d").execute().get("messages", [])]
n = {"found": len(ids), "created": 0, "skipped": 0, "failed": 0}
when = lambda d: {"dateTime": d.isoformat(), "timeZone": "Europe/Paris"}
for mid in ids:
    try: title, start, end = parse(body(gm, mid))
    except (ValueError, KeyError, IndexError, StopIteration) as e: n["failed"] += 1; print("failed:", mid, repr(e)); continue
    if cal.events().list(calendarId="primary", privateExtendedProperty="gmail_id=" + mid).execute().get("items"): n["skipped"] += 1; continue
    cal.events().insert(calendarId="primary", body={"summary": title, "start": when(start), "end": when(end), "extendedProperties": {"private": {"gmail_id": mid}}}).execute(); n["created"] += 1
print(n)