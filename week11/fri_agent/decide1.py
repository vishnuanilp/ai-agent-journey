from datetime import datetime

def after_hours(ts, start, end):
    h = ts.hour
    if start > end:
        return h >= start or h < end
    return start <= h < end

def decide(people, ts, start, end):
    return people >= 1 and after_hours(ts, start, end)

for h in [14, 19, 22, 23, 2, 5, 8]:
    t = datetime(2026, 8, 11, h, 0)
    print(f"{h:02d}:00  people=1  ->  {decide(1, t, 22, 6)}")
    print(f"{h:02d}:00  people=0  ->  {decide(0, t, 22, 6)}")