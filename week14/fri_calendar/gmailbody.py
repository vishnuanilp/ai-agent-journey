import base64

def body(gm, msg_id):
    msg = gm.users().messages().get(userId="me", id=msg_id, format="full").execute()
    parts = msg["payload"].get("parts", [msg["payload"]])
    plain = next(p for p in parts if p["mimeType"] == "text/plain")
    return base64.urlsafe_b64decode(plain["body"]["data"] + "==").decode("utf-8")