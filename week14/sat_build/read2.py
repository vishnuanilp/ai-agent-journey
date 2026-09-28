from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

RULE = "subject:(interview OR application OR recruiter OR offer) newer_than:7d"
NAME = "Vocview/Job"

def read_and_label():
    gm = build("gmail", "v1", credentials=Credentials.from_authorized_user_file("token.json")).users()
    ids = [m["id"] for m in gm.messages().list(userId="me", q=RULE).execute().get("messages", [])]
    lab = next((l for l in gm.labels().list(userId="me").execute()["labels"] if l["name"] == NAME), None)
    if lab is None:
        lab = gm.labels().create(userId="me", body={"name": NAME}).execute()
    if ids:
        gm.messages().batchModify(userId="me", body={"ids": ids, "addLabelIds": [lab["id"]]}).execute()
    rows = []
    for i in ids:
        heads = gm.messages().get(userId="me", id=i, format="metadata", metadataHeaders=["From", "Date", "Subject"]).execute()["payload"]["headers"]
        rows.append({"id": i} | {h["name"]: h["value"] for h in heads})
    total = gm.labels().get(userId="me", id=lab["id"]).execute()["messagesTotal"]
    return rows, total

if __name__ == "__main__":
    rows, total = read_and_label()
    print("found", len(rows), "|", NAME, "total", total)
    for r in rows:
        print(" ", r.get("Date"), "|", r.get("From"), "|", r.get("Subject"))