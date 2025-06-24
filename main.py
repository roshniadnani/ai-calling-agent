import os
import subprocess
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel

# Emergency install for Vonage (in case it's missing)
try:
    import vonage
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "vonage==2.6.0"])
    import vonage

# Your internal modules
from gpt_elevenlabs import generate_voice
from google_sheets import append_row_to_sheet
from call_vonage import make_call

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")

session_state = {}

questions = [
    "Can I confirm your full name?",
    "What is your full street address, including city and ZIP code?",
    # ... (the rest of your question list) ...
    "What time works best for your appointment?",
]

def ncco_stream_and_input(mp3_url):
    return [
        {"action": "stream", "streamUrl": [mp3_url], "loop": 0},
        {"action": "input",
         "eventUrl": [f"{RENDER_BASE_URL}/webhooks/event"],
         "speech": {"timeout": 5, "endOnSilence": True},
         "dtmf": {"maxDigits": 1, "timeout": 5}}
    ]

@app.post("/webhooks/answer")
def answer_call():
    greeting = "Hi, this is Desiree from Millennium Information Services. I’ll be conducting a quick home interview for insurance purposes. Is now a good time to talk?"
    path = "static/desiree_response.mp3"
    generate_voice(greeting, output_path=path)
    url = f"{RENDER_BASE_URL}/{path}"
    return JSONResponse(content=ncco_stream_and_input(url))

@app.post("/webhooks/event")
async def handle_event(request: Request):
    payload = await request.json()
    uuid = payload.get("uuid")
    speech = payload.get("speech", {}).get("text")
    dtmf = payload.get("dtmf", {}).get("digits")
    user_input = speech or dtmf or ""

    state = session_state.setdefault(uuid, {"step": 0, "answers": []})
    state["answers"].append(user_input)
    step = state["step"]
    state["step"] += 1

    if state["step"] < len(questions):
        q = questions[state["step"]]
        filename = f"static/response_{uuid}.mp3"
        generate_voice(q, output_path=filename)
        url = f"{RENDER_BASE_URL}/{filename}"
        return JSONResponse(content=ncco_stream_and_input(url))
    else:
        append_row_to_sheet(state["answers"])
        farewell = "Thanks! Your answers are recorded, and a representative will follow up soon."
        filename = f"static/response_{uuid}.mp3"
        generate_voice(farewell, output_path=filename)
        url = f"{RENDER_BASE_URL}/{filename}"
        session_state.pop(uuid, None)
        return JSONResponse(content=[{"action": "stream", "streamUrl": [url]}])

@app.get("/")
def root():
    return {"message": "✅ AI Calling Agent Live"}

class CallRequest(BaseModel):
    to_number: str

@app.post("/call")
def trigger_outbound_call(request: CallRequest):
    print(f"📞 Triggering call to: {request.to_number}")
    ok = make_call(request.to_number)
    return {"status": "ok" if ok else "error"}
