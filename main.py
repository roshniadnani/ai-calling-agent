from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from call_vonage import make_call
from gpt_elevenlabs import generate_gpt_reply, generate_voice

load_dotenv()

app = FastAPI()

# Serve static folder for audio streaming
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"message": "AI Calling Agent is running."}


@app.get("/make-call/{to_number}")
def call_user(to_number: str):
    make_call(to_number)
    return {"status": "Call initiated", "number": to_number}


@app.post("/webhooks/answer")
async def answer_call(request: Request):
    prompt = "Hello, this is Desiree, your AI insurance agent. Let's begin your quick insurance survey."
    
    gpt_response = generate_gpt_reply(prompt)
    audio_filename = generate_voice(gpt_response)  # should return 'desiree_output.mp3'

    render_url = os.getenv("RENDER_BASE_URL")  # e.g. https://ai-calling-agent-xxx.onrender.com
    audio_url = f"{render_url}/static/{audio_filename}"

    ncco = [
        {
            "action": "stream",
            "streamUrl": [audio_url]
        }
    ]
    return JSONResponse(content=ncco)


@app.post("/webhooks/events")
async def events(request: Request):
    payload = await request.json()
    print("Vonage Event Received:", payload)
    return {"status": "Event received"}
