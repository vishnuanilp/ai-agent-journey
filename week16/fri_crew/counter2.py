import httpx
from collections import Counter

HTTP = Counter()
_send = httpx.Client.send

def _counted_send(self, request, *args, **kwargs):
    if "openai.com" in request.url.host:
        HTTP[request.url.path] += 1
    return _send(self, request, *args, **kwargs)

httpx.Client.send = _counted_send
