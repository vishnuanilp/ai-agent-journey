from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

resp = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input="ഈ ഹോട്ടലിൽ പ്രഭാതഭക്ഷണം എട്ട് മണിക്ക് ആരംഭിക്കും."
)

resp.stream_to_file("openai_mal.wav")
print("written")