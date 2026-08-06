import os
from dotenv import load_dotenv
from supabase import create_client
from usable import frame_usable
from sharp import sharpness
from runners import ask_gemini, parse

load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
OWNER = "6c4986bc-e2a6-4e4a-aaf2-bea7a2e0875c"
MAX_PEOPLE = 5
FRAMES = ["frames/clean_text.jpg", "frames/blurry.jpg", "frames/dark_person.jpg"]

for path in FRAMES:
    gate = frame_usable(path)
    row = {"owner_id": OWNER, "frame_name": path.split("/")[-1],
           "crushed": round(gate["crushed"], 4),
           "sharpness": round(sharpness(path), 2),
           "person_present": None, "person_count": None}
    if not gate["frame_usable"]:
        row["outcome"], row["reason"] = "rejected", gate["reason"]
    else:
        try:
            raw = ask_gemini(path)[0]
        except Exception as e:
            row["outcome"] = "unknown"
            row["reason"] = f"{type(e).__name__}: {e}"
        else:
            data = parse(raw)
            row["person_present"] = data["person_present"]
            row["person_count"] = None if data["person_count"] > MAX_PEOPLE else data["person_count"]
            row["outcome"] = "person" if data["person_present"] else "no_person"
            row["reason"] = "ok"
    sb.table("events").insert(row).execute()
    print(f'{row["frame_name"]:18} {row["outcome"]:10} crushed {row["crushed"]}  sharp {row["sharpness"]}')