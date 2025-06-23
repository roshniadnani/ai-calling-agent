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
VONAGE_VIRTUAL_NUMBER = os.getenv("VONAGE_VIRTUAL_NUMBER")  # Fixed name
VONAGE_PRIVATE_KEY_PATH = os.getenv("VONAGE_PRIVATE_KEY_PATH")
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")

# ✅ Load private key from file
def load_private_key():
    if not VONAGE_PRIVATE_KEY_PATH or not os.path.exists(VONAGE_PRIVATE_KEY_PATH):
        raise FileNotFoundError("❌ VONAGE_PRIVATE_KEY_PATH is missing or invalid.")
    with open(VONAGE_PRIVATE_KEY_PATH, "r") as file:
        return file.read()

# ✅ Generate JWT for Vonage Auth
def generate_jwt():
    private_key = load_private_key()
    payload = {
        "application_id": VONAGE_APPLICATION_ID,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "jti": f"jwt-{int(time.time())}"
    }
    return jwt.encode(payload, private_key, algorithm="RS256")

# ✅ Make the outbound call
def make_call(to_number):
    print(f"📞 Initiating call to: {to_number}")
    url = "https://api.nexmo.com/v1/calls"
    headers = {
        "Authorization": f"Bearer {generate_jwt()}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": [{"type": "phone", "number": to_number}],
        "from": {"type": "phone", "number": VONAGE_VIRTUAL_NUMBER},
        "answer_url": [f"{RENDER_BASE_URL}/webhooks/answer"],
        "event_url": [f"{RENDER_BASE_URL}/webhooks/event"]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"✅ Call API Status: {response.status_code} - {response.text}")
        return response.status_code == 201
    except Exception as e:
        print(f"❌ Call failed: {e}")
        return False
