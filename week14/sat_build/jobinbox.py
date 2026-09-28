import subprocess, sys
from read2 import read_and_label, NAME
from analyse3 import analyse
from send4 import send_digest

def main():
    rows, total = read_and_label()
    df, by_sender, by_day = analyse(rows)
    subprocess.run([sys.executable, "digest1.py", "14"], check=True)
    extra = f"\nJOB MAIL ({NAME})\n  label total {total} | rows {len(df)}\n"
    extra += "".join(f"  sender {s}: {n}\n" for s, n in by_sender.items())
    extra += "".join(f"  day {d}: {n}\n" for d, n in by_day.items())
    with open("digest.txt", "a", encoding="utf-8") as f:
        f.write(extra)
    subject, msg_id, labels, chars = send_digest()
    print("sent:", subject, "|", msg_id, "|", labels, "| chars", chars)

if __name__ == "__main__":
    main()