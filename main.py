import os
import json
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from gpt_elevenlabs import generate_voice

app = FastAPI()
load_dotenv()

VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_APPLICATION_ID = os.getenv("VONAGE_APPLICATION_ID")
VONAGE_PRIVATE_KEY_PATH = os.getenv("VONAGE_PRIVATE_KEY_PATH")
VONAGE_NUMBER = os.getenv("VONAGE_NUMBER")
BASE_URL = os.getenv("BASE_URL")  # e.g., https://ai-calling-agent-xxxx.onrender.com

session_state = {}

class CallRequest(BaseModel):
    to_number: str

@app.post("/call")
def trigger_outbound_call(request: CallRequest):
    print("📞 /call received for:", request.to_number)
    jwt = generate_jwt()
    print("🔐 JWT generated.")
    url = "https://api-us-3.vonage.com/v1/calls"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json"
    }
    body = {
        "to": [{"type": "phone", "number": request.to_number}],
        "from": {"type": "phone", "number": VONAGE_NUMBER},
        "ncco": [
            {"action": "talk", "text": "Hi, this is Desiree. Can we talk for a minute?"},
            {"action": "input", "eventUrl": [f"{BASE_URL}/webhooks/event"]}
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    print("📤 Vonage response:", response.status_code, response.text)
    return {"status": response.status_code, "details": response.json()}

@app.post("/webhooks/event")
async def handle_event(request: Request):
    data = await request.json()
    print("📩 Webhook event:", data)

    uuid = data.get("uuid") or data.get("conversation_uuid")
    if not uuid:
        return {"error": "Missing uuid"}

    state = session_state.setdefault(uuid, {"idx": 0, "answers": []})

    if data.get("speech"):
        text = data["speech"].get("results", [{}])[0].get("text", "")
        state["answers"].append(text)
        print("🗣️ User said:", text)

    prompts = ["How are you feeling today?", "Do you want to hear some news?", "Would you like to talk again later?"]
    idx = state["idx"]

    if idx < len(prompts):
        reply = prompts[idx]
        state["idx"] += 1
    else:
        reply = "It was great talking. Goodbye!"

    filename = f"static/reply_{uuid}.mp3"
    generate_voice(reply, filename)

    return {
        "action": "play",
        "streamUrl": [f"{BASE_URL}/{filename}"]
    }

@app.get("/webhooks/answer")
def handle_answer(request: Request):
    return {
        "ncco": [
            {"action": "talk", "text": "Hi, this is Desiree."},
            {"action": "input", "eventUrl": [f"{BASE_URL}/webhooks/event"]}
        ]
    }

def generate_jwt():
    import jwt
    from time import time

    with open(VONAGE_PRIVATE_KEY_PATH, "r") as f:
        private_key = f.read()

    payload = {
        "application_id": VONAGE_APPLICATION_ID,
        "iat": int(time()),
        "exp": int(time()) + 60,
        "jti": os.urandom(8).hex()
    }

    return jwt.encode(payload, private_key, algorithm="RS256")
