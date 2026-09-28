import base64
from datetime import datetime
from email.message import EmailMessage
from zoneinfo import ZoneInfo
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ME = "v.vocview@gmail.com"

def send_digest(path="digest.txt"):
    text = open(path, encoding="utf-8").read()
    subject = "Vocview morning digest " + datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d %H:%M")
    msg = EmailMessage()
    msg["To"], msg["From"], msg["Subject"] = ME, ME, subject
    msg.set_content(text)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    gm = build("gmail", "v1", credentials=Credentials.from_authorized_user_file("token.json")).users()
    sent = gm.messages().send(userId="me", body={"raw": raw}).execute()
    check = gm.messages().get(userId="me", id=sent["id"], format="minimal").execute()
    return subject, sent["id"], check["labelIds"], len(text)

if __name__ == "__main__":
    subject, msg_id, labels, chars = send_digest()
    print("subject:", subject)
    print("id:", msg_id, "| labels from Gmail:", labels, "| body chars:", chars)