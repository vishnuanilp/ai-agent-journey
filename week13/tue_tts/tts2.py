from transformers import pipeline
import soundfile as sf

tts = pipeline("text-to-speech", model="facebook/mms-tts-eng")

TEXT = "The hotel offers roomservice frombasic varioustypes uponrequest."

out = tts(TEXT)

sf.write("broken.wav", out["audio"].T, out["sampling_rate"])
print(out["audio"].shape[0] / out["sampling_rate"], "seconds")
print("written")