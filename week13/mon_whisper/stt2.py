import whisper
model = whisper.load_model("base")
result = model.transcribe("clinic.wav")
print("KEYS:", result.keys())
print("LANGUAGE:", result["language"])
for seg in result["segments"]:
    print(round(seg["start"],2), "->", round(seg["end"],2), "|", seg["text"])