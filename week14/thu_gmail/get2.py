from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
WANT = ["From", "Subject", "Date"]
creds = Credentials.from_authorized_user_file("token.json", SCOPES)
service = build("gmail", "v1", credentials=creds)
gmail = service.users().messages()

msgs = gmail.list(userId="me", maxResults=5).execute().get("messages", [])
got = 0
for m in msgs:
    r = gmail.get(userId="me", id=m["id"], format="metadata",
                  metadataHeaders=WANT).execute()
    h = {x["name"]: x["value"] for x in r["payload"]["headers"]}
    got += 1
    print(got, h.get("From", "")[:35], "|", h.get("Subject", "")[:35])
print("listed:", len(msgs), "got:", got)