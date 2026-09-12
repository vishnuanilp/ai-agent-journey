import sys
sys.path.append(r"..\mon_whisper")
from listen import listen
print(listen("mic11.wav"))