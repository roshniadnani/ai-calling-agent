import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")  # zWRDoH56JB9twPHdkksW
MODEL_ID = os.getenv("ELEVEN_MODEL_ID", "eleven_monolingual_v1")

if not ELEVEN_API_KEY or not DESIREE_VOICE_ID:
    raise EnvironmentError("❌ Missing ElevenLabs API key or voice ID")

client = ElevenLabs(api_key=ELEVEN_API_KEY)

def generate_voice(text: str, output_path="static/desiree_response.mp3"):
    try:
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id=DESIREE_VOICE_ID,
            model_id=MODEL_ID,
            output_format="mp3_44100_128",
            optimize_streaming_latency="4"
        )
        with open(output_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
        print(f"✅ Audio saved to {output_path}")
    except Exception as e:
        print(f"❌ Error generating voice: {e}")
