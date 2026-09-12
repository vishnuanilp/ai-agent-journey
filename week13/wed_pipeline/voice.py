import sys
sys.path.append(r"..\mon_whisper")
sys.path.append(r"..\tue_tts")
import winsound
from record import record
from listen import listen
from think import think
from speak import speak

def converse(seconds=10, out_path="answer.wav"):
    q_path = record("q.wav", seconds)
    text, lang = listen(q_path)
    print("HEARD :", repr(text), "| LANG:", lang)
    reply = think(text)
    print("SAID  :", reply)
    path = speak(reply, "en", out_path)
    winsound.PlaySound(path, winsound.SND_FILENAME)
    return path

if __name__ == "__main__":
    print(converse())