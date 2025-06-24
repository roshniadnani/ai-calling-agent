from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from elevenlabs import generate, save, set_api_key
import os
import uuid
from vonage import Voice
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Load environment variables
APPLICATION_ID = os.getenv("VONAGE_APPLICATION_ID")
PRIVATE_KEY_PATH = os.getenv("VONAGE_PRIVATE_KEY_PATH")
VIRTUAL_NUMBER = os.getenv("VONAGE_VIRTUAL_NUMBER")
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
DESIREE_VOICE_ID = os.getenv("DESIREE_VOICE_ID")

# Setup ElevenLabs
set_api_key(ELEVEN_API_KEY)

# Load Vonage credentials
with open(PRIVATE_KEY_PATH, "r") as f:
    private_key = f.read()

voice = Voice(application_id=APPLICATION_ID, private_key=private_key)


@app.post("/call")
async def call_user(request: Request):
    data = await request.json()
    to_number = data.get("to")
    if not to_number:
        return JSONResponse({"error": "Missing 'to' number"}, status_code=400)

    try:
        response = voice.create_call({
            "to": [{"type": "phone", "number": to_number}],
            "from": {"type": "phone", "number": VIRTUAL_NUMBER},
            "answer_url": [f"{RENDER_BASE_URL}/answer"],
            "event_url": [f"{RENDER_BASE_URL}/event"]
        })
        return {"message": "Call initiated", "response": response}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/answer")
async def answer():
    script_text = (
        "Hi! This is Desiree, your insurance advisor. I'm calling to walk you through a quick quote. "
        "It will only take a minute. May I begin? "
        "Great! First, can you confirm your full name and date of birth?"
    )
    filename = f"audio_{uuid.uuid4().hex}.mp3"
    audio = generate(text=script_text, voice=DESIREE_VOICE_ID, model="eleven_monolingual_v1")
    save(audio, filename)
    return JSONResponse([
        {
            "action": "stream",
            "streamUrl": [f"{RENDER_BASE_URL}/static/{filename}"]
        }
    ])


@app.post("/event")
async def event_handler(request: Request):
    data = await request.json()
    print("📞 Call event received:", data)
    return JSONResponse({"status": "received"})
