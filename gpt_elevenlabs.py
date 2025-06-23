import os
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

# Load environment variables from .env
load_dotenv()

# Get keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")

# Set API clients
if not OPENAI_API_KEY or not ELEVEN_API_KEY:
    raise EnvironmentError("❌ Missing OpenAI or ElevenLabs API keys.")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVEN_API_KEY)

def generate_gpt_reply(prompt: str) -> str:
    """Returns a natural language response from GPT-4 based on the prompt."""
    try:
        system_prompt = (
            "You are Desiree, a professional, warm and helpful insurance representative. "
            "Ask clear questions in a natural tone and never mention AI."
        )

        chat_completion = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print("❌ GPT Error:", e)
        return "Sorry, I'm having trouble generating a response right now."

def generate_voice(text: str, output_path="static/desiree_response.mp3"):
    """Generates MP3 audio using Desiree's ElevenLabs voice."""
    try:
        audio = eleven_client.generate(
            text=text,
            voice=DESIREE_VOICE_ID,
            model="eleven_monolingual_v1",
            voice_settings=VoiceSettings(stability=0.4, similarity_boost=0.8)
        )
        with open(output_path, "wb") as f:
            f.write(audio)
        print(f"✅ Audio saved to {output_path}")
    except Exception as e:
        print("❌ ElevenLabs audio error:", e)
