from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
Q = "from:tm.openai.com newer_than:30d"
LABEL = "Label_1"

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
gmail = build("gmail", "v1", credentials=creds).users().messages()

hits = gmail.list(userId="me", q=Q).execute().get("messages", [])
print("matched:", len(hits))

for m in hits:
    gmail.modify(userId="me", id=m["id"], body={"addLabelIds": [LABEL]}).execute()

after = gmail.list(userId="me", q="label:Vocview/Checked").execute().get("messages", [])
print("wearing label:", len(after))