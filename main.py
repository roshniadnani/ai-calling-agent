import os
import subprocess
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel

# Emergency install for Vonage
try:
    import vonage
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "vonage==2.6.3"])
    import vonage

from gpt_elevenlabs import generate_voice
from google_sheets import append_row_to_sheet
from call_vonage import make_call

load_dotenv()

# Generate opening greeting once on startup
generate_voice(
    "Hi, this is Desiree from Millennium Information Services. I’ll be conducting a quick home interview for insurance purposes. Is now a good time to talk?",
    "static/desiree_response.mp3"
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")
session_state = {}

questions = [
    "Can I confirm your full name?",
    "What is your full street address, including city and ZIP code?",
    "What is your date of birth?",
    "Can I get a phone number for follow-up?",
    "Do you have an email address we can use for your policy information?",
    "What type of insurance policy are you applying for?",
    "What level of coverage are you interested in?",
    "Do you currently have insurance on your property?",
    "Is the property occupied full-time or part-time?",
    "How many people currently reside in the home?",
    "What year was the home built?",
    "What is the home’s approximate square footage?",
    "Are there any known damages or renovations ongoing?",
    "Would you like to book an appointment to speak with an agent?",
    "What time works best for your appointment?",
]

@app.get("/")
def home():
    return {"message": "AI Calling Agent Live"}

@app.get("/webhooks/answer")
def answer_call():
    public_url = f"{RENDER_BASE_URL}/static/desiree_response.mp3"
    ncco = [{"action": "stream", "streamUrl": [public_url]}]
    return JSONResponse(content=ncco)

@app.post("/webhooks/event")
async def handle_event(request: Request):
    data = await request.json()

    # Safe uuid handling
    uuid = data.get("uuid") or data.get("conversation_uuid") or "default"

    # Safe session state
    global session_state
    if not isinstance(session_state, dict):
        session_state = {}
    state = session_state.setdefault(uuid, {"idx": 0, "answers": []})

    # Capture user input
    speech = data.get("speech", {}).get("text")
    dtmf = data.get("dtmf", {}).get("digits")
    user_input = speech or dtmf or "..."

    state["answers"].append(user_input)
    state["idx"] += 1

    audio_path = f"static/response_{uuid}.mp3"

    if state["idx"] >= len(questions):
        append_row_to_sheet(state["answers"])
        generate_voice("Thank you! Your answers have been recorded. A representative will follow up with you soon.", audio_path)
        session_state.pop(uuid, None)
    else:
        next_q = questions[state["idx"]]
        generate_voice(next_q, audio_path)

    return {"status": "ok"}

@app.get("/webhooks/next")
def serve_next(uuid: str):
    audio_path = f"static/response_{uuid}.mp3"
    if os.path.exists(audio_path):
        return JSONResponse(content=[{
            "action": "stream",
            "streamUrl": [f"{RENDER_BASE_URL}/webhooks/next-audio?uuid={uuid}"]
        }])
    return JSONResponse(content={"error": "Audio not ready"}, status_code=404)

@app.get("/webhooks/next-audio")
def stream_audio(uuid: str):
    path = f"static/response_{uuid}.mp3"
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    return JSONResponse(content={"error": "File not found"}, status_code=404)

class CallRequest(BaseModel):
    to_number: str

@app.post("/call")
def trigger_outbound_call(request: CallRequest):
    print(f"📞 /call received for: {request.to_number}")
    success = make_call(request.to_number)
    return {"status": "ok" if success else "error"}
