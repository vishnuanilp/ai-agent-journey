from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
WANT = ["From", "Subject", "Date"]

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
service = build("gmail", "v1", credentials=creds)

res = service.users().messages().list(userId="me", maxResults=5).execute()
msgs = res.get("messages", [])
print("listed:", len(msgs))

for m in msgs:
    full = service.users().messages().get(
        userId="me", id=m["id"], format="metadata", metadataHeaders=WANT
    ).execute()
    heads = full["payload"]["headers"]
    print(len(heads), [h["name"] for h in heads])