import os
import requests
from elevenlabs import generate, save, Voice, VoiceSettings
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")  # zWRDoH56JB9twPHdkksW

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_gpt_reply(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Desiree, a warm and helpful American voice assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def generate_voice(text, filename="desiree_output.mp3"):
    audio = generate(
        text=text,
        voice=Voice(
            voice_id=DESIREE_VOICE_ID,
            settings=VoiceSettings(stability=0.4, similarity_boost=0.7)
        ),
        api_key=ELEVENLABS_API_KEY
    )
    save(audio, filename)
    print(f"✅ Audio saved: {filename}")
