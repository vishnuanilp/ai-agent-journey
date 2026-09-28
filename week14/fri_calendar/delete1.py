from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

cal = build("calendar", "v3", credentials=Credentials.from_authorized_user_file("token.json"))

EVENT_ID = "lc7iboar8l8r3hkg3a2n89fgb4"
reply = cal.events().delete(calendarId="primary", eventId=EVENT_ID).execute()
print("deleted:", EVENT_ID, "| reply:", repr(reply))