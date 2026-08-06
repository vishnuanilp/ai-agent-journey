from PIL import Image

DARK_LEVEL = 40
BLOWN_LEVEL = 240
CRUSHED_MAX = 0.25
BLOWN_MAX = 0.25

def frame_usable(path):
    grey = Image.open(path).convert("L")
    hist = grey.histogram()
    total = sum(hist)
    crushed = sum(hist[:DARK_LEVEL]) / total
    blown = sum(hist[BLOWN_LEVEL:]) / total
    ok = crushed <= CRUSHED_MAX and blown <= BLOWN_MAX
    reason = "ok" if ok else ("too_dark" if crushed > CRUSHED_MAX else "too_bright")
    return {"frame_usable": ok, "reason": reason,
            "crushed": round(crushed, 3), "blown": round(blown, 3)}