import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load credentials
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # fallback

if not ELEVEN_API_KEY:
    raise EnvironmentError("❌ Missing ELEVEN_API_KEY in .env file")

def generate_speech(text: str, filename: str = "desiree_response.mp3") -> str | None:
    """
    Sends text to ElevenLabs and saves streamed MP3 to /static.
    Returns path to saved audio or None on error.
    """
    if not text:
        raise ValueError("❗ Cannot synthesize empty text.")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{DESIREE_VOICE_ID}/stream"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.8
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            os.makedirs("static", exist_ok=True)
            output_path = os.path.join("static", filename)
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Audio saved to: {output_path}")
            return output_path
        else:
            print(f"❌ ElevenLabs error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception during TTS request: {e}")
        return None

# Local test
if __name__ == "__main__":
    generate_speech("Hello! This is Desiree from Millennium. I’m calling to complete your phone interview.")
