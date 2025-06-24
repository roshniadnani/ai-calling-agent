import os
import subprocess
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel

# Ensure vonage is installed
try:
    import vonage
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "vonage==2.6.3"])
    import vonage

# Your helper modules
from gpt_elevenlabs import generate_voice
from google_sheets import append_row_to_sheet
from call_vonage import make_call

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")
session_state = {}
questions = [
    # ... your question list as before
]

def build_ncco_stream(uuid: str):
    return [{"action": "stream", "streamUrl": [f"{RENDER_BASE_URL}/webhooks/next-audio?uuid={uuid}"]},
            {"action": "input", "eventUrl": [f"{RENDER_BASE_URL}/webhooks/event"], "timeout": 10, "bargeIn": True}]

@app.post("/webhooks/answer")
def answer_call(request: Request):
    greeting = questions[0]
    generate_voice(greeting, output_path=f"static/response_temp.mp3")
    return JSONResponse(build_ncco_stream("temp"))

@app.post("/webhooks/event")
async def handle_event(request: Request):
    payload = await request.json()
    uuid = payload.get("uuid")
    user_input = (payload.get("speech") or {}).get("text") or \
                 (payload.get("dtmf") or {}).get("digits") or ""

    state = session_state.setdefault(uuid, {"step": 0, "answers": []})
    state["answers"].append(user_input)
    step = state["step"] + 1

    if step >= len(questions):
        append_row_to_sheet(state["answers"])
        farewell = "Thank you! A rep will call you shortly. Goodbye!"
        generate_voice(farewell, f"static/response_{uuid}.mp3")
        session_state.pop(uuid, None)
        return JSONResponse([{"action": "stream", "streamUrl": [f"{RENDER_BASE_URL}/webhooks/next-audio?uuid={uuid}"]}])
    else:
        next_q = questions[step]
        generate_voice(next_q, f"static/response_{uuid}.mp3")
        session_state[uuid]["step"] = step
        return JSONResponse(build_ncco_stream(uuid))

@app.get("/webhooks/next-audio")
def next_audio(uuid: str):
    path = f"static/response_{uuid}.mp3"
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    return JSONResponse({"error": "File not ready"}, status_code=404)

class CallRequest(BaseModel):
    to_number: str

@app.post("/call")
def outbound(request: CallRequest):
    ok = make_call(request.to_number)
    return {"status": "ok" if ok else "error"}
