import os
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs import generate, save, VoiceSettings, set_api_key

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")

# Validate
if not OPENAI_API_KEY or not ELEVEN_API_KEY or not DESIREE_VOICE_ID:
    raise EnvironmentError("❌ Missing OpenAI or ElevenLabs credentials in .env")

# Configure clients
client = OpenAI(api_key=OPENAI_API_KEY)
set_api_key(ELEVEN_API_KEY)

def generate_gpt_reply(prompt: str) -> str:
    """Generates human-like reply as Desiree using GPT-4."""
    try:
        system_prompt = (
            "You are Desiree, a professional, warm and helpful insurance representative. "
            "Ask clear follow-up questions and speak naturally. Avoid AI references."
        )

        chat = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        return chat.choices[0].message.content.strip()
    except Exception as e:
        print("❌ GPT error:", e)
        return "Sorry, I'm having trouble generating a response."

def generate_voice(text: str, output_path="static/desiree_response.mp3"):
    """Converts response to speech using Desiree’s voice."""
    try:
        audio = generate(
            text=text,
            voice=DESIREE_VOICE_ID,
            model="eleven_monolingual_v1",
            voice_settings=VoiceSettings(
                stability=0.4,
                similarity_boost=0.8
            )
        )
        save(audio, output_path)
        print(f"✅ Audio saved to {output_path}")
    except Exception as e:
        print("❌ ElevenLabs audio error:", e)
