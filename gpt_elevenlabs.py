# gpt_elevenlabs.py

import os
from elevenlabs import generate, save, Voice, VoiceSettings, set_api_key

# ✅ Get API key from environment variable
api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    raise EnvironmentError("ELEVENLABS_API_KEY is not set")
set_api_key(api_key)

# ✅ Generates audio file using ElevenLabs
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

# ✅ Dummy GPT response function (to simulate actual generation)
def generate_gpt_reply(prompt):
    # Replace this with real logic later
    return f"Hi! You said: {prompt}. I'm Desiree. How can I help?"
