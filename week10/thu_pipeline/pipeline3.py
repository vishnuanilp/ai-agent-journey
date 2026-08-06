from usable import frame_usable
from runners import ask_gemini, parse

FRAMES = ["frames/clean_text.jpg", "frames/blurry.jpg", "frames/dark_person.jpg"]

for path in FRAMES:
    gate = frame_usable(path)
    if not gate["frame_usable"]:
        print(path, "-> REJECTED |", gate["reason"])
        continue
    text, secs = ask_gemini(path)
    data = parse(text)
    print(path, "-> present:", data["person_present"], "| count:", data["person_count"])