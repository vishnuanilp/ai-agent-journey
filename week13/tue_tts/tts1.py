from transformers import pipeline
import soundfile as sf

tts = pipeline("text-to-speech", model="facebook/mms-tts-eng")

out = tts("The fish curry today is karimeen.")

print(type(out))
print(out.keys())
print(out["sampling_rate"])
print(out["audio"].shape)

sf.write("eng.wav", out["audio"].T, out["sampling_rate"])
print("written")