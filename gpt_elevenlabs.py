# gpt_elevenlabs.py

import os
from elevenlabs import Voice, VoiceSettings, play, save, generate
from elevenlabs import set_api_key

# ✅ Get API key from environment and set it
api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    raise EnvironmentError("ELEVENLABS_API_KEY environment variable is not set")
set_api_key(api_key)

def generate_voice(text: str, voice_name="Desiree", file_path="static/desiree_response.mp3"):
    try:
        audio = generate(
            text=text,
            voice=Voice(
                voice_id="EXAVITQu4vr4xnSDxMaL",  # Desiree
                settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
            )
        )
        save(audio, file_path)
        print(f"✅ Audio saved to {file_path}")
        return file_path
    except Exception as e:
        print(f"❌ Error generating voice: {e}")
        return None
