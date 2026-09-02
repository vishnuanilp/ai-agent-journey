from urllib.parse import urlparse

BLOCKED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254"}

def check_url(raw):
    u = urlparse(raw)
    if u.scheme not in ("http", "https"):
        return False, f"scheme not allowed: {u.scheme or 'none'}"
    if not u.hostname:
        return False, "no hostname"
    if u.hostname.lower() in BLOCKED_HOSTS:
        return False, f"blocked host: {u.hostname}"
    return True, "ok"

for raw in ["https://bellacucina.in/reviews", "htp://bellacucina.in",
            "file:///C:/Users/vishn/.env", "http://localhost:8000/evil.html",
            "javascript:alert(1)"]:
    ok, why = check_url(raw)
    print(f"{'ALLOW' if ok else 'REJECT':6} | {why:32} | {raw}")