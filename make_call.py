import os
import time
import jwt
import requests
from dotenv import load_dotenv

load_dotenv()

VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_APPLICATION_ID = os.getenv("VONAGE_APPLICATION_ID")
VONAGE_VIRTUAL_NUMBER = os.getenv("VONAGE_VIRTUAL_NUMBER")
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")
VONAGE_PRIVATE_KEY = os.getenv("VONAGE_PRIVATE_KEY")

def generate_jwt():
    if not VONAGE_PRIVATE_KEY or not VONAGE_APPLICATION_ID:
        raise ValueError("Missing credentials")
    payload = {
        "application_id": VONAGE_APPLICATION_ID,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "jti": "ai-calling-agent-jwt"
    }
    return jwt.encode(payload, VONAGE_PRIVATE_KEY, algorithm="RS256")

def make_call(to_number):
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
    return requests.post(url, headers=headers, json=payload).json()
