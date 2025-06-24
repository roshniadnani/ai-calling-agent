import os
from elevenlabs import generate, set_api_key

set_api_key(os.getenv("ELEVEN_API_KEY"))

def generate_voice(text: str, output_path: str = "static/output.mp3"):
    audio = generate(
        text=text,
        voice=os.getenv("DESIREE_VOICE_ID"),
        model="eleven_monolingual_v1"
    )
    with open(output_path, "wb") as f:
        f.write(audio)
