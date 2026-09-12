import whisper
model = whisper.load_model("base")
result = model.transcribe("clinic.wav")
print(result["text"])