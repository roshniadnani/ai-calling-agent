import os
from elevenlabs import generate, set_api_key
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set ElevenLabs API Key
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # fallback ID

if not ELEVEN_API_KEY:
    raise EnvironmentError("❌ ELEVEN_API_KEY is missing from your .env")

set_api_key(ELEVEN_API_KEY)

def generate_voice(text: str, output_path: str = "static/output.mp3"):
    """
    Generate MP3 audio using ElevenLabs and save to static/ directory.
    """
    if not text:
        raise ValueError("❗ Text input for voice generation is empty.")

    try:
        audio = generate(
            text=text,
            voice=DESIREE_VOICE_ID,
            model="eleven_monolingual_v1"
        )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(audio)
        print(f"✅ MP3 generated and saved to {output_path}")
    except Exception as e:
        print(f"❌ Error generating voice: {e}")
        raise
