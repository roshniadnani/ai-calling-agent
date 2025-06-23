import os
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs import generate, save, VoiceSettings, set_api_key

# Load environment variables
load_dotenv()

# Get keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")  # zWRDoH56JB9twPHdkksW

# Set keys
if not OPENAI_API_KEY or not ELEVEN_API_KEY:
    raise EnvironmentError("❌ Missing OpenAI or ElevenLabs API key in .env")

client = OpenAI(api_key=OPENAI_API_KEY)
set_api_key(ELEVEN_API_KEY)

def generate_gpt_reply(prompt: str) -> str:
    """Generate a GPT-4 response for the user prompt."""
    try:
        system_prompt = (
            "You are Desiree, a warm and professional insurance assistant. "
            "Ask questions clearly and sound human. Never mention AI."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ GPT-4 Error:", e)
        return "Sorry, I'm unable to respond right now."

def generate_voice(text: str, output_path="static/desiree_response.mp3"):
    """Generate MP3 audio using ElevenLabs' voice."""
    try:
        audio = generate(
            text=text,
            voice=DESIREE_VOICE_ID,
            model="eleven_monolingual_v1",
            voice_settings=VoiceSettings(stability=0.4, similarity_boost=0.8)
        )
        save(audio, output_path)
        print(f"✅ Saved audio to {output_path}")
    except Exception as e:
        print("❌ ElevenLabs audio error:", e)
