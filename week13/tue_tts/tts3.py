from transformers import pipeline
import soundfile as sf

tts = pipeline("text-to-speech", model="facebook/mms-tts-mal")

TEXT = "ഈ ഹോട്ടലിൽ പ്രഭാതഭക്ഷണം എട്ട് മണിക്ക് ആരംഭിക്കും."

out = tts(TEXT)

sf.write("mal.wav", out["audio"].T, out["sampling_rate"])
print(out["sampling_rate"])
print(out["audio"].shape[0] / out["sampling_rate"], "seconds")
print("written")