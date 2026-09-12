from transformers import pipeline

stt = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small"
)

print("pipeline built")
print(type(stt))
print(stt.model.config.model_type)
print(stt.model.num_parameters())