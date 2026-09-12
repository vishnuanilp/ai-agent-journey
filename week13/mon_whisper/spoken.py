import re

def spoken_to_url(text):
    t = text.lower().strip().rstrip(".?!")
    t = t.replace(" dot ", ".").replace(" slash ", "/")
    t = t.replace(" dash ", "-").replace(" underscore ", "_")
    t = re.sub(r"\s+", "", t)
    if not t:
        return None
    if not t.startswith(("http://", "https://")):
        t = "https://" + t
    return t

if __name__ == "__main__":
    print(spoken_to_url("wikipedia dot org slash wiki slash clinic"))