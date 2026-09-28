from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file("token.json")
cal = build("calendar", "v3", credentials=creds)

event = {
    "summary": "Vocview test event",
    "start": {"dateTime": "2026-10-06T14:00:00", "timeZone": "Europe/Paris"},
    "end": {"dateTime": "2026-10-06T14:45:00", "timeZone": "Europe/Paris"},
}

made = cal.events().insert(calendarId="primary", body=event).execute()
print("id:", made["id"])
print("start:", made["start"])