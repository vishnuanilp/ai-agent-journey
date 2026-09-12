import whisper
m = whisper.load_model("small")
r = m.transcribe("q.wav", language="en")
print(repr(r["text"]))