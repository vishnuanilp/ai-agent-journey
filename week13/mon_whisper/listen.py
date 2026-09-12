import whisper
_model = None
def listen(path, language="en"):
    global _model
    if _model is None:
        _model = whisper.load_model("small")
    r = _model.transcribe(path, language=language)
    return r["text"].strip(), r["language"]
if __name__ == "__main__":
    print(listen("url.wav"))