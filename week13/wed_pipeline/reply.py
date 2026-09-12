import sys
sys.path.append(r"..\tue_tts")
import winsound
from speak import speak
from think import think

def answer(question, lang="en", out_path="reply.wav"):
    text = think(question)
    print("SAID  :", text)
    path = speak(text, lang, out_path)
    print("WROTE :", path)
    winsound.PlaySound(path, winsound.SND_FILENAME)
    return path

if __name__ == "__main__":
    answer("Do you take walk-ins on Sunday?")