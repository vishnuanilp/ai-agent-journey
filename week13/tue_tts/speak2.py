import time
from speak import speak

t0 = time.time()
speak("The hotel restaurant opens at seven.", "en", "t1.wav")
t1 = time.time()

speak("The kitchen closes at eleven.", "en", "t2.wav")
t2 = time.time()

print("first  call:", round(t1 - t0, 2), "s")
print("second call:", round(t2 - t1, 2), "s")