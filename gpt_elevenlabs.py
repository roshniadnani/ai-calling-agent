# gpt_elevenlabs.py

import os
from elevenlabs import generate, save, Voice, VoiceSettings, set_api_key

# ✅ Get API key from environment variable
api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    raise EnvironmentError("ELEVENLABS_API_KEY is not set")
set_api_key(api_key)

# ✅ Generates audio file using ElevenLabs
from elevenlabs import generate, save, Voice, VoiceSettings, set_api_key
import os

set_api_key(os.getenv("ELEVENLABS_API_KEY"))

def generate_voice(text, output_path="static/desiree_response.mp3"):
    audio = generate(
        text=text,
        voice=Voice(
            voice_id="EXAVITQu4vr4xnSDxMaL",  # Replace with Desiree's actual ID if different
            settings=VoiceSettings(stability=0.45, similarity_boost=0.7)
        ),
        model="eleven_monolingual_v1"
    )
    save(audio, output_path)
    return output_path
