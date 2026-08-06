from usable import frame_usable
from runners import ask_gemini, parse

MAX_PEOPLE = 5          # chosen for this camera, not measured

FRAMES = ["frames/clean_text.jpg", "frames/blurry.jpg", "frames/dark_person.jpg"]

for path in FRAMES:
    gate = frame_usable(path)
    if not gate["frame_usable"]:
        print(path, "-> rejected |", gate["reason"])
        continue
    data = parse(ask_gemini(path)[0])
    count = data["person_count"]
    if count > MAX_PEOPLE:
        count = None
    outcome = "person" if data["person_present"] else "no_person"
    print(path, "->", outcome, "| count:", count)