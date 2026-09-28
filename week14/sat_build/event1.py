from parse1 import role, start, end
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

cal = build("calendar", "v3", credentials=Credentials.from_authorized_user_file("token.json"))
GMAIL_ID = "1a0e2cda501842a2"
found = cal.events().list(calendarId="primary", privateExtendedProperty="gmail_id=" + GMAIL_ID).execute().get("items", [])
if found: raise SystemExit("skipped: already in calendar as " + found[0]["id"])
event = {"summary": "Interview - " + role,
         "start": {"dateTime": start.isoformat(), "timeZone": "Europe/Paris"},
         "end": {"dateTime": end.isoformat(), "timeZone": "Europe/Paris"},
         "extendedProperties": {"private": {"gmail_id": GMAIL_ID}}}
made = cal.events().insert(calendarId="primary", body=event).execute()
print("created:", made["id"], "|", made["start"]["dateTime"])