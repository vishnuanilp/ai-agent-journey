import base64
from pathlib import Path

FRAME = Path("frames/room_person.jpg")

raw_bytes = FRAME.read_bytes()
print("original bytes :", len(raw_bytes))

b64_string = base64.b64encode(raw_bytes).decode("utf-8")
print("base64 chars   :", len(b64_string))

data_url = f"data:image/jpeg;base64,{b64_string}"
print("data url head  :", data_url[:80])