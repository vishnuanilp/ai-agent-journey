from transformers import pipeline

WAV = r"..\mon_whisper\url.wav"

stt = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small"
)

result = stt(WAV)

print(type(result))
print(result)