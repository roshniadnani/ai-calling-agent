import os
import openai
from elevenlabs import play, save, VoiceSettings, Voice, generate
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")


def generate_gpt_reply(prompt):
    print("🧠 Generating GPT reply for prompt:", prompt)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Desiree, a warm, polite American insurance agent."},
            {"role": "user", "content": prompt}
        ]
    )
    reply = response.choices[0].message["content"]
    print("✅ GPT reply:", reply)
    return reply


def generate_voice(text, filename="desiree_output.mp3"):
    from elevenlabs.client import ElevenLabs

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    audio = client.generate(
        text=text,
        voice=Voice(voice_id=DESIREE_VOICE_ID),
        model="eleven_multilingual_v2",
        stream=False,
        output_format="mp3_44100_128"
    )

    output_path = os.path.join(os.getcwd(), filename)
    save(audio, output_path)
    print(f"🎧 Audio saved at: {output_path}")
    return output_path
