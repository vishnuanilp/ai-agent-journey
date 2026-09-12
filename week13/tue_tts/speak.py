from transformers import pipeline
import soundfile as sf

MODELS = {"en": "facebook/mms-tts-eng", "ml": "facebook/mms-tts-mal"}
_pipes = {}

def speak(text, lang="en", out_path="speech.wav"):
    if lang not in _pipes:
        _pipes[lang] = pipeline("text-to-speech", model=MODELS[lang])
    out = _pipes[lang](text)
    sf.write(out_path, out["audio"].T, out["sampling_rate"])
    return out_path

if __name__ == "__main__":
    print(speak("Breakfast starts at eight.", "en", "demo_en.wav"))