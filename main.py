import os
import subprocess
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv
from pydantic import BaseModel

# Emergency install fix (for Render)
try:
    import vonage
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "vonage==2.6.0"])
    import vonage

from gpt_elevenlabs import generate_gpt_reply, generate_voice
from google_sheets import append_row_to_sheet
from call_vonage import make_call

load_dotenv()
app = FastAPI()
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")

# In-memory session store
session_state = {}

# Call script questions
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
def root():
    return {"message": "✅ AI Calling Agent Live with Multi-Turn Script"}

@app.post("/webhooks/answer")
def answer_call():
    greeting = "Hi, this is Desiree from Millennium Information Services. I’ll be conducting a quick home interview for insurance purposes. Is now a good time to talk?"
    output_path = "static/desiree_response.mp3"
    generate_voice(greeting, output_path=output_path)
    ncco = [{"action": "stream", "streamUrl": [f"{RENDER_BASE_URL}/static/desiree_response.mp3"]}]
    return JSONResponse(content=ncco)

@app.post("/webhooks/event")
async def handle_event(request: Request):
    payload = await request.json()
    uuid = payload.get("uuid")
    speech = payload.get("speech", {}).get("text")
    dtmf = payload.get("dtmf", {}).get("digits")
    user_input = speech or dtmf or "..."

    if uuid not in session_state:
        session_state[uuid] = {"step": 0, "answers": []}

    state = session_state[uuid]
    step = state["step"]
    state["answers"].append(user_input)
    state["step"] += 1

    audio_path = f"static/response_{uuid}.mp3"

    if state["step"] >= len(questions):
        append_row_to_sheet(state["answers"])
        farewell = "Thank you! Your answers have been recorded. A representative will follow up with you soon."
        generate_voice(farewell, output_path=audio_path)
        session_state.pop(uuid, None)
    else:
        next_question = questions[state["step"]]
        generate_voice(next_question, output_path=audio_path)

    return {"status": "ok"}

@app.get("/webhooks/next")
def serve_next(uuid: str):
    audio_path = f"static/response_{uuid}.mp3"
    if os.path.exists(audio_path):
        return JSONResponse(content=[{
            "action": "stream",
            "streamUrl": [f"{RENDER_BASE_URL}/webhooks/next-audio?uuid={uuid}"]
        }])
    return JSONResponse(content={"error": "Response audio not ready."}, status_code=404)

@app.get("/webhooks/next-audio")
def stream_mp3(uuid: str):
    path = f"static/response_{uuid}.mp3"
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    return {"error": "File not found"}

# Outbound Call Trigger API
class CallRequest(BaseModel):
    to_number: str

@app.post("/webhooks/answer")
async def answer_call(request: Request):
    print("📞 /webhooks/answer hit from Vonage")

    greeting = "Hi, this is Desiree from Millennium Information Services. I’ll be conducting a quick home interview for insurance purposes. Is now a good time to talk?"
    output_path = "static/desiree_response.mp3"
    generate_voice(greeting, output_path=output_path)

    public_url = f"{RENDER_BASE_URL}/static/desiree_response.mp3"
    print(f"✅ Serving audio from: {public_url}")

    ncco = [{"action": "stream", "streamUrl": [public_url]}]
    return JSONResponse(content=ncco)
