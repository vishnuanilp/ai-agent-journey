from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file("token.json")
cal = build("calendar", "v3", credentials=creds)

now = datetime.now(timezone.utc).isoformat()
res = cal.events().list(calendarId="primary", timeMin=now, singleEvents=True,
                        orderBy="startTime", maxResults=10).execute()
items = res.get("items", [])
for e in items:
    print(e["start"].get("dateTime", e["start"].get("date")), "|", e.get("summary"))
print("total:", len(items), "| test:", sum(e.get("summary") == "Vocview test event" for e in items), "| more:", "nextPageToken" in res)