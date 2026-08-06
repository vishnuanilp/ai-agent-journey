import os, uuid
from datetime import datetime, timezone
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pipeline import process_frame

UPLOADS = "uploads"
app = FastAPI()

PAGE = """<h2>Vocview — footage ingest</h2>
<form action="/upload" method="post" enctype="multipart/form-data">
  <input type="file" name="frame">
  <button type="submit">Check this frame</button>
</form>"""


def page_with(msg):
    return f"<p><b>{msg}</b></p>" + PAGE


@app.get("/", response_class=HTMLResponse)
def form():
    return PAGE


@app.post("/upload", response_class=HTMLResponse)
def upload(frame: UploadFile = File(...)):
    if not frame.filename:
        return page_with("No file chosen — pick a frame first.")
    data = frame.file.read()
    if not data:
        return page_with(f"{frame.filename} is empty (0 bytes) — nothing to check.")
    received = datetime.now(timezone.utc).isoformat()
    safe = f"{uuid.uuid4().hex[:8]}_{os.path.basename(frame.filename)}"
    path = os.path.join(UPLOADS, safe)
    with open(path, "wb") as f:
        f.write(data)
    row = process_frame(path, received)
    return (f"<h2>{row['frame_name']}</h2>"
            f"<p>outcome: <b>{row['outcome']}</b></p>"
            f"<p>received: {row['received_at']}</p>"
            f"<p>reason: {row['reason']}</p>"
            f"<p>crushed {row['crushed']} · sharpness {row['sharpness']}</p>"
            f"<p>person_present: {row['person_present']} · count: {row['person_count']}</p>"
            f'<p><a href="/">another frame</a></p>')