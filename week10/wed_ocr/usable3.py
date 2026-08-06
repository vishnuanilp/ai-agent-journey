from usable import frame_usable

for name in ["clean_text.jpg", "dark_person.jpg", "blurry.jpg"]:
    print(name, frame_usable(f"frames/{name}"))
    