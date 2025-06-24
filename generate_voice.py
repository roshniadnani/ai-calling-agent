import os
import requests
from dotenv import load_dotenv

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")

def generate_voice(text: str, output_path: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{DESIREE_VOICE_ID}/stream"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.85
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"🎤 Audio saved: {output_path}")
        return output_path
    else:
        print("❌ ElevenLabs error:", response.status_code, response.text)
        return None
