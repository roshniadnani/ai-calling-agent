import os
from elevenlabs import generate, save, Voice, VoiceSettings, set_api_key

# Setup API key
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

def generate_voice(text, output_path="static/desiree_response.mp3"):
    audio = generate(
        text=text,
        voice=Voice(
            voice_id="EXAVITQu4vr4xnSDxMaL",  # Replace with correct Desiree voice ID if needed
            settings=VoiceSettings(stability=0.45, similarity_boost=0.7)
        ),
        model="eleven_monolingual_v1"
    )
    save(audio, output_path)
    return output_path
