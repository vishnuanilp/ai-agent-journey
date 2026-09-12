from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url("https://en.wikipedia.org/robots.txt")
rp.read()

tests = [
    "https://en.wikipedia.org/wiki/Kerala",
    "https://en.wikipedia.org/w/index.php?title=Kerala&action=edit",
]

for t in tests:
    print(rp.can_fetch("*", t), "|", t)