import os
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from gpt_elevenlabs import generate_voice
from vonage import Voice
import json

load_dotenv()

app = FastAPI()
voice = Voice(key=os.getenv("VONAGE_API_KEY"), secret=os.getenv("VONAGE_API_SECRET"))
VONAGE_NUMBER = os.getenv("VONAGE_NUMBER")
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")
VOICE_NAME = os.getenv("VOICE_NAME", "Rachel")

session_state = {}

@app.post("/call")
async def trigger_outbound_call(request: Request):
    data = await request.json()
    to_number = data.get("to")
    print(f"📞 /call received for: {to_number}")

    ncco_url = f"{RENDER_BASE_URL}/webhooks/answer"

    response = voice.create_call({
        "to": [{"type": "phone", "number": to_number}],
        "from": {"type": "phone", "number": VONAGE_NUMBER},
        "answer_url": [ncco_url],
        "event_url": [f"{RENDER_BASE_URL}/webhooks/event"]
    })

    print(f"✅ Call successfully initiated.")
    return JSONResponse(content=response)

@app.get("/webhooks/answer")
async def answer_call(request: Request):
    caller_uuid = str(uuid.uuid4())
    session_state[caller_uuid] = {"idx": 0, "answers": []}

    public_url = f"{RENDER_BASE_URL}/static/desiree_response.mp3"
    ncco = [
        {"action": "stream", "streamUrl": [public_url]},
        {
            "action": "input",
            "eventUrl": [f"{RENDER_BASE_URL}/webhooks/event"],
            "speech": {"language": "en-US", "endOnSilence": 1, "maxDuration": 5},
            "dtmf": {"maxDigits": 1, "timeOut": 5}
        }
    ]
    return JSONResponse(content=ncco)

@app.post("/webhooks/event")
async def handle_event(request: Request):
    data = await request.json()
    print("🔁 Webhook event received")
    print(f"Headers: {request.headers}")
    print(f"🔹 Body: {json.dumps(data)}")

    uuid = data.get("uuid")
    if not uuid:
        return JSONResponse(status_code=200, content={"message": "No UUID"})

    state = session_state.get(uuid)
    if not state:
        state = session_state.setdefault(uuid, {"idx": 0, "answers": []})

    # Simulate next message
    next_text = "Thank you for your response. We'll be in touch."
    file_path = f"static/response_{uuid}.mp3"
    generate_voice(next_text, file_path)

    public_url = f"{RENDER_BASE_URL}/{file_path}"
    ncco = [
        {"action": "stream", "streamUrl": [public_url]},
        {
            "action": "input",
            "eventUrl": [f"{RENDER_BASE_URL}/webhooks/event"],
            "speech": {"language": "en-US", "endOnSilence": 1, "maxDuration": 5},
            "dtmf": {"maxDigits": 1, "timeOut": 5}
        }
    ]
    return JSONResponse(content=ncco)

@app.get("/")
async def root():
    return {"message": "AI Calling Agent is Live"}
