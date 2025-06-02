import os
import openai
from elevenlabs import generate, save
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
agent_url = os.getenv("DESIREE_AGENT_URL")

def generate_gpt_reply(user_input):
    prompt = f"""
You are Desiree, a kind and helpful American female insurance agent from Millennium Information Services.

Follow this script strictly, one step at a time:

1. Start with: "Hi, this is Desiree calling on behalf of Millennium Information Services. I’d like to verify some information to help process your insurance request. May I confirm a few quick details?"

2. Then go through the script from the Homesite-360-HVR-MVR-Phone-Interview document, question-by-question.

3. Wait for the user to answer before continuing (in the real app, the system handles this).

4. Speak naturally and professionally. Do not answer for the user. Ask clearly, and never rush.

Current conversation so far:
{user_input}

Continue as Desiree with the next appropriate question from the script:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']


def generate_voice(text):
    audio = generate(
        api_key=elevenlabs_api_key,
        agent_id="PU6B8gfYqp3DrePOTFvu",
        text=text,
        model="eleven_monolingual_v1"
    )

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    audio_path = f"output/audio_{timestamp}.mp3"
    save(audio, audio_path)
    return audio_path
