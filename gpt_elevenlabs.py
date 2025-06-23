import os
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs import VoiceClient, VoiceSettings, set_api_key, text_to_speech

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")  # Use this for Desiree

if not OPENAI_API_KEY or not ELEVEN_API_KEY or not DESIREE_VOICE_ID:
    raise EnvironmentError("Missing keys or voice ID in .env.")

client = OpenAI(api_key=OPENAI_API_KEY)
set_api_key(ELEVEN_API_KEY)
voice_client = VoiceClient()

def generate_gpt_reply(prompt: str) -> str:
    system = "You are Desiree, a professional, warm and helpful insurance representative."
    resp = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return resp.choices[0].message.content.strip()

def generate_voice(text: str, output_path="static/desiree_response.mp3"):
    try:
        audio_bytes = voice_client.text_to_speech(
            text=text,
            voice=DESIREE_VOICE_ID,
            voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
        )
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        print(f"✅ Audio saved to {output_path}")
    except Exception as e:
        print("❌ ElevenLabs audio error:", e)
