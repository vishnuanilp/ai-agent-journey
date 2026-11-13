import httpx, httpx2
from collections import Counter

# Prices per 1M tokens: (input, cache read, output, cache write 5m). Checked 12 Nov 2026:
# developers.openai.com/api/docs/pricing · platform.claude.com/docs/en/about-claude/pricing
PRICES = {
    "gpt-4o-mini":            (0.15, 0.075, 0.60,  0.15),
    "text-embedding-3-small": (0.02, 0.02,  0.00,  0.02),
    "claude-sonnet-5-5":      (2.00, 0.10,  10.00, 2.50),
}
HOSTS = ("openai.com", "anthropic.com")

HTTP = Counter()   # path -> calls
ROWS = []          # one dict per call: path, model, tin, cached, cwrite, tout, cost

def _price(model):
    for name, p in PRICES.items():
        if model.startswith(name):
            return p
    return None

def _log(request, response):
    row = {"path": request.url.path, "model": "?", "tin": 0,
           "cached": 0, "cwrite": 0, "tout": 0, "cost": None}
    try:
        body = response.json()
        u = body.get("usage") or {}
        row["model"] = body.get("model", "?")
        if "input_tokens" in u:    # Claude: input_tokens EXCLUDES cache reads AND cache writes
            row["cached"] = u.get("cache_read_input_tokens") or 0
            row["cwrite"] = u.get("cache_creation_input_tokens") or 0
            row["tin"] = u["input_tokens"] + row["cached"] + row["cwrite"]
            row["tout"] = u.get("output_tokens", 0)
        else:                      # OpenAI: prompt_tokens INCLUDES cached
            row["cached"] = (u.get("prompt_tokens_details") or {}).get("cached_tokens") or 0
            row["tin"] = u.get("prompt_tokens", 0)
            row["tout"] = u.get("completion_tokens", 0)
        p = _price(row["model"])
        if p and u:
            fresh = row["tin"] - row["cached"] - row["cwrite"]
            row["cost"] = (fresh * p[0] + row["cached"] * p[1] + row["tout"] * p[2]
                           + row["cwrite"] * p[3]) / 1e6
    except Exception:
        row["model"] = "UNREAD"
    ROWS.append(row)

def _wrap(real_send):
    def _logged_send(self, request, *args, **kwargs):
        response = real_send(self, request, *args, **kwargs)
        if request.url.host.endswith(HOSTS):
            HTTP[request.url.path] += 1
            _log(request, response)
        return response
    return _logged_send

httpx.Client.send = _wrap(httpx.Client.send)     # OpenAI SDK + CrewAI
httpx2.Client.send = _wrap(httpx2.Client.send)   # anthropic 2.8.0 uses httpx2
