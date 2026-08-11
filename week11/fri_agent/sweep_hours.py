from datetime import datetime, timedelta
from decide1 import decide

def count(began, fps, n_frames, people, start, end):
    fired = 0
    for n in range(1, n_frames + 1):
        ts = began + timedelta(seconds=n / fps)
        if decide(people, ts, start, end):
            fired += 1
    return fired

clip = (datetime(2026, 8, 9, 19, 46), 11.0, 110, 1)
empty = (datetime(2026, 8, 11, 17, 56), 24.5, 245, 0)

print("start end | clip empty")
for start, end in [(22,6),(21,6),(20,6),(19,6),(18,6),(17,6),(19,20),(17,18)]:
    print(f" {start:02d}   {end:02d}  | {count(*clip,start,end):4d} {count(*empty,start,end):5d}")