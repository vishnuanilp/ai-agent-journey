from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
NAME = "Vocview/Checked"

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
api = build("gmail", "v1", credentials=creds).users().labels()

have = {l["name"]: l["id"] for l in api.list(userId="me").execute()["labels"]}
print("labels before:", len(have))

if NAME in have:
    print("already exists:", have[NAME])
else:
    new = api.create(userId="me", body={"name": NAME}).execute()
    print("created:", new["id"], new["name"])