import os
from elevenlabs import generate, save, Voice, VoiceSettings
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")

# GPT Reply Generator
def generate_gpt_reply(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Desiree, a professional AI insurance agent. Speak clearly and kindly."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# ElevenLabs Voice Generator
def generate_voice(text: str, filename: str = "desiree_output.mp3") -> str:
    audio = generate(
        text=text,
        voice=Voice(voice_id=DESIREE_VOICE_ID),
        model="eleven_multilingual_v2",
        api_key=ELEVENLABS_API_KEY,
        voice_settings=VoiceSettings(stability=0.7, similarity_boost=0.9)
    )

    output_path = os.path.join("static", filename)
    save(audio, output_path)
    return filename
