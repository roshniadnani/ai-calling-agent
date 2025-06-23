# main.py (final)

import os, subprocess, sys
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel

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
session_state = []

questions = [
  # ... your earlier questionnaire ...
]

@app.post("/webhooks/answer")
def answer_call():
    greeting = "Hi, this is Desiree from Millennium Information Services. I’ll be conducting a quick home interview…"
    generate_voice(greeting, output_path="static/desiree_initial.mp3")
    public_url = f"{RENDER_BASE_URL}/static/desiree_initial.mp3"

    ncco = [
      {"action": "stream", "streamUrl": [public_url]},
      {"action": "pause", "length": 7}
    ]
    return JSONResponse(content=ncco)

@app.post("/webhooks/event")
async def handle_event(request: Request):
    data = await request.json()
    uuid = data["uuid"]
    resp_text = (data.get("speech") or {}).get("text") or (data.get("dtmf") or {}).get("digits", "")
    state = session_state.setdefault(uuid, {"idx": 0, "answers": []})
    state["answers"].append(resp_text or "...")

    if state["idx"] >= len(questions):
        append_row_to_sheet(state["answers"])
        finish = "Thank you. A representative will reach out shortly."
        generate_voice(finish, output_path=f"static/{uuid}_done.mp3")
        ncco = [
          {"action": "stream", "streamUrl": [f"{RENDER_BASE_URL}/static/{uuid}_done.mp3"]},
          {"action": "pause", "length": 3}
        ]
        session_state.pop(uuid, None)
        return JSONResponse(content=ncco)
    else:
        ask = questions[state["idx"]]
        state["idx"] += 1
        generate_voice(ask, output_path=f"static/{uuid}_q.mp3")
        ncco = [
          {"action": "stream", "streamUrl": [f"{RENDER_BASE_URL}/static/{uuid}_q.mp3"]},
          {"action": "pause", "length": 7}
        ]
        return JSONResponse(content=ncco)

@app.get("/webhooks/next-audio")
def next_audio(uuid: str):
    path = f"static/{uuid}_q.mp3"
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    return {"error": "not_ready"}

class CallRequest(BaseModel):
    to_number: str

@app.post("/call")
def trigger(request: CallRequest):
    return {"ok": make_call(request.to_number)}
