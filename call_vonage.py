import os
import time
import jwt
import requests
from dotenv import load_dotenv

load_dotenv()

# Load Vonage credentials from .env
VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_APPLICATION_ID = os.getenv("VONAGE_APPLICATION_ID")
VONAGE_VIRTUAL_NUMBER = os.getenv("VONAGE_VIRTUAL_NUMBER")
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")
VONAGE_PRIVATE_KEY = os.getenv("VONAGE_PRIVATE_KEY")

def generate_jwt():
    try:
        if not VONAGE_PRIVATE_KEY or not VONAGE_APPLICATION_ID:
            raise ValueError("❌ Missing VONAGE_PRIVATE_KEY or APPLICATION_ID in environment.")

        payload = {
            "application_id": VONAGE_APPLICATION_ID,
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,
            "jti": "ai-calling-agent-jwt"
        }

        token = jwt.encode(payload, VONAGE_PRIVATE_KEY, algorithm="RS256")
        print("🔐 JWT generated successfully.")
        return token
    except Exception as e:
        print(f"❌ Error generating JWT: {e}")
        raise

def make_call(to_number):
    print(f"📞 Initiating call to: {to_number}")
    try:
        url = "https://api.nexmo.com/v1/calls"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {generate_jwt()}"
        }

        payload = {
            "to": [{"type": "phone", "number": to_number}],
            "from": {"type": "phone", "number": VONAGE_VIRTUAL_NUMBER},
            "answer_url": [f"{RENDER_BASE_URL}/webhooks/answer"],
            "event_url": [f"{RENDER_BASE_URL}/webhooks/event"]
        }

        print("📤 Sending request to Vonage...")
        response = requests.post(url, headers=headers, json=payload)

        print(f"🔹 Status: {response.status_code}")
        print(f"🔹 Headers: {response.headers}")
        print(f"🔹 Body: {response.text}")

        if response.status_code == 201:
            print("✅ Call successfully initiated.")
        else:
            print("⚠️ Failed to initiate call.")
        return response.status_code == 201

    except Exception as e:
        print(f"❌ Vonage call failed: {e}")
        return False
