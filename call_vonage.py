import os
import requests
from dotenv import load_dotenv

load_dotenv()

VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_APPLICATION_ID = os.getenv("VONAGE_APPLICATION_ID")
VONAGE_VIRTUAL_NUMBER = os.getenv("VONAGE_VIRTUAL_NUMBER")
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")

def make_call(to_number):
    print("TO NUMBER SENT:", to_number)
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

    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code, response.text)

def generate_jwt():
    import jwt
    import time

    private_key = os.getenv("VONAGE_PRIVATE_KEY")
    if not private_key:
        raise ValueError("Missing VONAGE_PRIVATE_KEY in environment.")

    payload = {
        "application_id": VONAGE_APPLICATION_ID,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "jti": "my-jwt"
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token
