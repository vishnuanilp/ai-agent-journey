from usable import frame_usable
from runners import ask_gemini

FRAMES = [
    "frames/clean_text.jpg",
    "frames/blurry.jpg",
    "frames/dark_person.jpg",
]

for path in FRAMES:
    gate = frame_usable(path)
    if not gate["frame_usable"]:
        print(path, "-> REJECTED |", gate["reason"])
        continue
    text, secs = ask_gemini(path)
    print(path, "-> RAW:", repr(text), "|", round(secs, 1), "s")