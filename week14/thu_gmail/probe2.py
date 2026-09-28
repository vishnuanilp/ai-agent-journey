from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
QUERIES = ["newer_than:30d", "from:openai.com newer_than:30d",
           "from:tm.Anthropic.com newer_than:30d", "from:google.com newer_than:30d",
           "subject:account newer_than:30d", "after:2026/09/20 before:2026/09/27"]

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
gmail = build("gmail", "v1", credentials=creds).users().messages()

for q in QUERIES:
    res = gmail.list(userId="me", q=q, maxResults=100).execute()
    print(f"{len(res.get('messages', [])):4}  {q}")