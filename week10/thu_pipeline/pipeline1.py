from usable import frame_usable

FRAMES = [
    "frames/clean_text.jpg",
    "frames/blurry.jpg",
    "frames/dark_person.jpg",
]

for path in FRAMES:
    gate = frame_usable(path)
    if not gate["frame_usable"]:
        print(path, "-> REJECTED |", gate["reason"], "| crushed", round(gate["crushed"], 3))
        continue
    print(path, "-> PASSED   | crushed", round(gate["crushed"], 3))