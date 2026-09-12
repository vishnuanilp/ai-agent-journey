from transformers import pipeline

WAV = r"..\mon_whisper\url.wav"

stt = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small"
)

result = stt(WAV, return_timestamps=True)

print(result.keys())
print(result["text"])
for chunk in result["chunks"]:
    print(chunk)