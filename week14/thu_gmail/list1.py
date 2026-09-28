from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
service = build("gmail", "v1", credentials=creds)

res = service.users().messages().list(userId="me", maxResults=5).execute()
msgs = res.get("messages", [])

print("returned:", len(msgs))
print("keys:", list(res.keys()))
for m in msgs:
    print(m["id"])