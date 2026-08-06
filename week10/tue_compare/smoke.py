from runners import ask_openai, ask_claude, ask_gemini

frame = "frames/room_person.jpg"
for name, fn in [("openai", ask_openai),
                 ("claude", ask_claude),
                 ("gemini", ask_gemini)]:
    text, secs = fn(frame)
    print(f"{name:8} {secs:5.2f}s  {text!r}")