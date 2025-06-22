import os
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs import generate, save, VoiceSettings, set_api_key

# Load environment variables
load_dotenv()

# Get API keys from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")

# Validate required keys
if not OPENAI_API_KEY or not ELEVEN_API_KEY or not DESIREE_VOICE_ID:
    raise ValueError("❌ Missing one or more required API keys in the .env file.")

# Initialize clients
client = OpenAI(api_key=OPENAI_API_KEY)
set_api_key(ELEVEN_API_KEY)

# Generate GPT response
def generate_gpt_reply(prompt: str) -> str:
    system_prompt = (
        "You are Desiree, a warm and professional insurance interviewer representing "
        "Millennium Information Services. Speak clearly and naturally, as if you're a real human. "
        "Never say you're an AI or language model."
    )

    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return chat_completion.choices[0].message.content.strip()

# Generate and save audio
def generate_voice(text: str, output_path="static/desiree_output.mp3"):
    audio = generate(
        text=text,
        voice=DESIREE_VOICE_ID,
        model="eleven_monolingual_v1",
        voice_settings=VoiceSettings(
            stability=0.4,
            similarity_boost=0.85
        )
    )
    save(audio, output_path)
    print(f"✅ Voice response saved to {output_path}")
