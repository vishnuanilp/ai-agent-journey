import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

gm = build("gmail", "v1", credentials=Credentials.from_authorized_user_file("token.json"))
res = gm.users().messages().list(userId="me", q="subject:interview newer_than:7d").execute()
ids = [m["id"] for m in res.get("messages", [])]
print("found:", len(ids))
if not ids: raise SystemExit("no interview mail - stop")
msg = gm.users().messages().get(userId="me", id=ids[0], format="full").execute()
parts = msg["payload"].get("parts", [msg["payload"]])
plain = next(p for p in parts if p["mimeType"] == "text/plain")
text = base64.urlsafe_b64decode(plain["body"]["data"] + "==").decode("utf-8")
with open("body.txt", "w", encoding="utf-8", newline="") as f: f.write(text)
print("saved body.txt:", len(text), "characters | id:", ids[0])