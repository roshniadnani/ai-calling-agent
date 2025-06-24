import os
import uuid
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from gpt_elevenlabs import generate_voice
from vonage import Voice

# Load environment
load_dotenv()

app = FastAPI()

# Vonage setup
voice = Voice(key=os.getenv("VONAGE_API_KEY"), secret=os.getenv("VONAGE_API_SECRET"))
VONAGE_NUMBER = os.getenv("VONAGE_NUMBER")
RENDER_BASE_URL = "https://ai-calling-agent-9hv2.onrender.com"  # Live URL
VOICE_NAME = os.getenv("VOICE_NAME", "Desiree")

# Local call state memory
session_state = {}

@app.post("/call")
async def trigger_outbound_call(request: Request):
    data = await request.json()
    to_number = data.get("to")
    if not to_number:
        return JSONResponse(status_code=400, content={"error": "Missing 'to' number"})

    try:
        response = voice.create_call({
            "to": [{"type": "phone", "number": to_number}],
            "from": {"type": "phone", "number": VONAGE_NUMBER},
            "answer_url": [f"{RENDER_BASE_URL}/webhooks/answer"],
            "event_url": [f"{RENDER_BASE_URL}/webhooks/event"]
        })
        print("✅ Outbound call initiated.")
        return JSONResponse(content=response)
    except Exception as e:
        print(f"❌ Call initiation failed: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/webhooks/event")
async def handle_event(request: Request):
    data = await request.json()
    print("🔁 Vonage Event Received")
    print(json.dumps(data, indent=2))

    uuid_ = data.get("uuid")
    if not uuid_:
        return JSONResponse(content={"message": "No UUID"}, status_code=200)

    state = session_state.setdefault(uuid_, {"idx": 0, "answers": []})

    # Simulate agent response
    next_text = "Thank you for your response. We'll be in touch shortly."
    file_path = f"static/response_{uuid_}.mp3"
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
    return {"message": "✅ AI Calling Agent is Live"}

# ✅ Include router from call_vonage_play_audio.py
from call_vonage_play_audio import router as audio_router
app.include_router(audio_router)
