import os
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs import ElevenLabs, save

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DESIREE_AGENT_ID = os.getenv("DESIREE_AGENT_ID")  # use agent ID, not voice ID

# Generate GPT response
def generate_gpt_reply(prompt: str) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    chat = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Desiree, a professional AI insurance agent. Speak clearly and kindly."},
            {"role": "user", "content": prompt}
        ]
    )
    return chat.choices[0].message.content.strip()

# Generate ElevenLabs speech from agent
def generate_voice(text: str, filename: str = "desiree_output.mp3") -> str:
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=text,
        agent_id=DESIREE_AGENT_ID
    )

    output_path = os.path.join("static", filename)
    save(audio, output_path)
    return output_path
