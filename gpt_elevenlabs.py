import os
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs import generate, save, set_api_key

# Load environment variables
load_dotenv()

# Load keys
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate keys
if not ELEVEN_API_KEY or not DESIREE_VOICE_ID or not OPENAI_API_KEY:
    raise ValueError("❌ Missing one or more required API keys in the .env file.")

# Set API keys
set_api_key(ELEVEN_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

# Full phone interview script for Millennium Information Services
script_prompt = """
You are Desiree, a warm, friendly American woman working for Millennium Information Services.
You are calling homeowners to conduct a phone interview related to homeowners insurance.

Use the following professional and structured tone to follow the entire script step-by-step with pauses for user responses.

Begin now.
"""

# Generate GPT-4 response
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful insurance agent speaking on behalf of Millennium Information Services."},
        {"role": "user", "content": script_prompt}
    ],
    temperature=0.7
)

generated_text = response.choices[0].message.content.strip()
print("📝 GPT Output:\n", generated_text)

# Generate speech using ElevenLabs
audio = generate(
    text=generated_text,
    voice=DESIREE_VOICE_ID,
    model="eleven_monolingual_v1"
)

# Save audio
save(audio, "desiree_output.mp3")
print("✅ MP3 saved as desiree_output.mp3")
