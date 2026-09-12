from transformers import pipeline
import soundfile as sf

MODELS = {
    "en": "facebook/mms-tts-eng",
    "ml": "facebook/mms-tts-mal",
    "hi": "facebook/mms-tts-hin",
    "ta": "facebook/mms-tts-tam",
}
SCRIPTS = {
    "en": (0x0041, 0x007A),
    "ml": (0x0D00, 0x0D7F),
    "hi": (0x0900, 0x097F),
    "ta": (0x0B80, 0x0BFF),
}
_pipes = {}

def check_script(text, lang):
    lo, hi = SCRIPTS[lang]
    real = [ch for ch in text if ch.isalpha() or (lo <= ord(ch) <= hi)]
    hits = sum(1 for ch in real if lo <= ord(ch) <= hi)
    share = hits / len(real) if real else 0.0
    print("SCRIPT", lang, "MATCH", hits, "OF", len(real), "CHARS", round(share, 2))
    return share

def speak(text, lang="en", out_path="speech.wav"):
    if lang not in MODELS:
        raise ValueError(f"no model for '{lang}', have {list(MODELS)}")
    if check_script(text, lang) < 0.5:
        raise ValueError(f"text does not look like '{lang}' script")
    if lang not in _pipes:
        _pipes[lang] = pipeline("text-to-speech", model=MODELS[lang])
    out = _pipes[lang](text)
    sf.write(out_path, out["audio"].T, out["sampling_rate"])
    return out_path