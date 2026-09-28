from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
NAME = "Vocview/Recent30"
Q = "newer_than:30d"

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
api = build("gmail", "v1", credentials=creds).users()
labels, msgs = api.labels(), api.messages()

have = {l["name"]: l["id"] for l in labels.list(userId="me").execute()["labels"]}
lid = have.get(NAME) or labels.create(userId="me", body={"name": NAME}).execute()["id"]

ids = [m["id"] for m in msgs.list(userId="me", q=Q, maxResults=100).execute().get("messages", [])]
print("label:", lid, "  matched:", len(ids))

msgs.batchModify(userId="me", body={"ids": ids, "addLabelIds": [lid]}).execute()
after = msgs.list(userId="me", q=f"label:{NAME}", maxResults=100).execute().get("messages", [])
print("wearing label:", len(after))