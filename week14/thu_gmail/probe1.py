from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
QUERIES = ["newer_than:30d", "subject:job", "subject:application",
           "subject:interview", "category:updates newer_than:30d"]

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
gmail = build("gmail", "v1", credentials=creds).users().messages()

for q in QUERIES:
    res = gmail.list(userId="me", q=q, maxResults=100).execute()
    got = len(res.get("messages", []))
    more = "yes" if "nextPageToken" in res else "no"
    print(f"{got:4}  more={more:3}  {q}")