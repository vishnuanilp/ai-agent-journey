import os
from dotenv import load_dotenv
from supabase import create_client
from usable import frame_usable
from sharp import sharpness
from runners import ask_openai, parse

load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
OWNER = "6c4986bc-e2a6-4e4a-aaf2-bea7a2e0875c"
MAX_PEOPLE = 5


def process_frame(path, received_at=None):
    row = {"owner_id": OWNER, "frame_name": os.path.basename(path),
           "received_at": received_at,
           "crushed": None, "sharpness": None,
           "person_present": None, "person_count": None}
    try:
        gate = frame_usable(path)
        row["crushed"] = round(gate["crushed"], 4)
        row["sharpness"] = round(sharpness(path), 2)
    except Exception as e:
        row["outcome"] = "rejected"
        row["reason"] = f"unreadable: {type(e).__name__}"
        sb.table("events").insert(row).execute()
        return row
    if not gate["frame_usable"]:
        row["outcome"], row["reason"] = "rejected", gate["reason"]
    else:
        try:
            raw = ask_openai(path)[0]
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
    return row


if __name__ == "__main__":
    for p in ["frames/clean_text.jpg", "frames/blurry.jpg", "frames/dark_person.jpg"]:
        r = process_frame(p)
        print(f'{r["frame_name"]:18} {r["outcome"]:10} crushed {r["crushed"]}  sharp {r["sharpness"]}')