import subprocess

DEVICE = "audio=Microphone (Realtek(R) Audio)"

def record(out_path="mic.wav", seconds=10):
    cmd = ["ffmpeg", "-f", "dshow", "-i", DEVICE,
           "-t", str(seconds), "-ar", "16000", "-ac", "1",
           "-y", "-loglevel", "error", out_path]
    print("SPEAK NOW -", seconds, "seconds")
    subprocess.run(cmd, check=True)
    print("RECORDED:", out_path)
    return out_path

if __name__ == "__main__":
    print(record("q.wav", 10))