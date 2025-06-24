import os
import subprocess
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel

# Emergency install for Vonage if missing
try:
    import vonage
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "vonage==2.6.3"])
    import vonage

from gpt_elevenlabs import generate_voice
from google_sheets import append_row_to_sheet
from call_vonage import make_call

# Load .env
load_dotenv()
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")

# Initialize app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory session storage
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
def root():
    return {"message": "✅ AI Calling Agent Live"}

# Incoming call answer webhook – play greeting, wait for input
@app.post("/webhooks/answer")
def answer_call(request: Request):
    greeting = questions[0]
    audio_path = "static/response_init.mp3"
    generate_voice(greeting, output_path=audio_path)
    ncco = [
        {
            "action": "stream",
            "streamUrl": [f"{RENDER_BASE_URL}/static/response_init.mp3"]
        },
        {
            "action": "input",
            "eventUrl": [f"{RENDER_BASE_URL}/webhooks/event"],
            "timeOut": 10,
            "maxDigits": 1
        }
    ]
    return JSONResponse(content=ncco)

# Event webhook – record reply, ask next question or end
@app.post("/webhooks/event")
async def handle_event(request: Request):
    payload = await request.json()
    uuid = payload.get("uuid")
    speech = payload.get("speech", {}).get("text")
    dtmf = payload.get("dtmf", {}).get("digits")
    answer = speech or dtmf or "<no reply>"

    state = session_state.setdefault(uuid, {"step": 0, "answers": []})
    state["answers"].append(answer)

    step = state["step"] + 1
    if step < len(questions):
        state["step"] = step
        question = questions[step]
        generate_voice(question, output_path=f"static/resp_{uuid}.mp3")
        ncco = [
            {"action": "stream", "streamUrl": [f"{RENDER_BASE_URL}/static/resp_{uuid}.mp3"]},
            {"action": "input", "eventUrl": [f"{RENDER_BASE_URL}/webhooks/event"], "timeOut": 10, "maxDigits": 1}
        ]
    else:
        append_row_to_sheet(state["answers"])
        farewell = "Thank you! A rep will follow up with you soon. Goodbye."
        generate_voice(farewell, output_path=f"static/resp_{uuid}.mp3")
        ncco = [{"action": "stream", "streamUrl": [f"{RENDER_BASE_URL}/static/resp_{uuid}.mp3"]}]
        session_state.pop(uuid, None)

    return JSONResponse(content=ncco)

# Trigger outbound call
class CallRequest(BaseModel):
    to_number: str

@app.post("/call")
def trigger_call(req: CallRequest):
    success = make_call(req.to_number)
    return {"status": "ok" if success else "error"}
