import os
import subprocess
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel

# Emergency Vonage install
try:
    import vonage
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "vonage==2.6.0"])
    import vonage

from gpt_elevenlabs import generate_voice
from google_sheets import append_row_to_sheet
from call_vonage import make_call

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")

# Maintain conversation state
session_state: dict[str, dict] = {}

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

# Root endpoint
@app.get("/")
def root():
    return {"message": "✅ AI Calling Agent Live"}


# Vonage answer webhook — first greeting
@app.post("/webhooks/answer")
def answer_call():
    greeting = (
        "Hi, this is Desiree from Millennium Information Services. "
        "I’ll be conducting a quick home interview for insurance purposes. "
        "Is now a good time to talk?"
    )
    output_path = "static/desiree_response.mp3"
    generate_voice(greeting, output_path=output_path)
    return JSONResponse([{"action": "stream", "streamUrl": [f"{RENDER_BASE_URL}/{output_path}"]}])

# Vonage event webhook — capturing responses and streaming next question
@app.post("/webhooks/event")
async def handle_event(request: Request):
    data = await request.json()
    uuid = data.get("uuid")
    speech = data.get("speech", {}).get("text")
    dtmf = data.get("dtmf", {}).get("digits")
    user_input = speech or dtmf or "..."
    print(f"💬 Event received (UUID {uuid}): '{user_input}'")

    if not uuid:
        return JSONResponse({"error": "Missing uuid"}, status_code=400)

    state = session_state.setdefault(uuid, {"step": 0, "answers": []})
    answers = state["answers"]
    answers.append(user_input)

    step = state["step"] = state["step"] + 1
    audio_path = f"static/response_{uuid}.mp3"

    if step >= len(questions):
        append_row_to_sheet(answers)
        farewell = (
            "Thank you! Your answers have been recorded. "
            "A representative will follow up with you soon."
        )
        generate_voice(farewell, output_path=audio_path)
        session_state.pop(uuid, None)
    else:
        next_q = questions[step]
        generate_voice(next_q, output_path=audio_path)

    return JSONResponse([{"action": "stream", "streamUrl": [f"{RENDER_BASE_URL}/{audio_path}"]}])


# Endpoint to pull latest audio (if needed)
@app.get("/webhooks/next-audio")
def stream_mp3(uuid: str):
    path = f"static/response_{uuid}.mp3"
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    return JSONResponse({"error": "File not ready"}, status_code=404)


# API to initiate outbound calls
class CallRequest(BaseModel):
    to_number: str

@app.post("/call")
def trigger_call(request: CallRequest):
    print(f"📞 /call for: {request.to_number}")
    success = make_call(request.to_number)
    return {"status": "ok" if success else "error"}
