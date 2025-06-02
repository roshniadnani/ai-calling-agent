import os
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs import generate, save, VoiceSettings, set_api_key

# Load environment variables
load_dotenv()

# Get API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# Validate
if not OPENAI_API_KEY or not ELEVEN_API_KEY:
    raise ValueError("❌ Missing one or more required API keys in the .env file.")

# Set API Keys
client = OpenAI(api_key=OPENAI_API_KEY)
set_api_key(ELEVEN_API_KEY)

def generate_gpt_reply(prompt: str) -> str:
    system_prompt = (
        "You are Desiree, a warm and professional insurance interviewer representing "
        "Millennium Information Services. Respond using polite, clear, and American tone. "
        "Don't say you're an AI."
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

def generate_voice(text: str, output_path="desiree_output.mp3"):
    audio = generate(
        text=text,
        voice="Rachel",
        model="eleven_monolingual_v1",
        voice_settings=VoiceSettings(stability=0.4, similarity_boost=0.8)
    )
    save(audio, output_path)
    print(f"✅ MP3 saved as {output_path}")
