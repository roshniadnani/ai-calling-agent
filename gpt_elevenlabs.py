import os
from dotenv import load_dotenv
import openai
from elevenlabs import generate, save

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("DESIREE_VOICE_ID")

def generate_gpt_reply(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response["choices"][0]["message"]["content"]
    print("GPT Reply:", reply)
    return reply

def generate_voice(text: str) -> str:
    audio = generate(
        text=text,
        voice=ELEVENLABS_VOICE_ID,
        model="eleven_monolingual_v1",
        api_key=ELEVENLABS_API_KEY
    )
    filename = "desiree_output.mp3"
    filepath = os.path.join("static", filename)
    save(audio, filepath)
    print(f"Voice saved to: {filepath}")
    return filename
