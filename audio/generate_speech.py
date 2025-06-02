
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
DESIREE_AGENT_ID = os.getenv("DESIREE_AGENT_ID")

def generate_speech(text: str, filename: str = "desiree_response.mp3"):
    url = f"https://api.elevenlabs.io/v1/agents/{DESIREE_AGENT_ID}/speech"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        output_path = os.path.join("static", filename)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Audio saved: {output_path}")
        return output_path
    else:
        print("❌ Error generating speech:", response.status_code, response.text)
        return None

# Test it
if __name__ == "__main__":
    generate_speech("Hello! This is Desiree from Millennium. I’m calling to complete your phone interview.")
