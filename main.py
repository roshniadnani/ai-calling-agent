import os
import subprocess
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Emergency pip install (Render-safe)
try:
    import vonage
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "vonage==2.6.0"])
    import vonage

# Load environment
load_dotenv()

app = FastAPI()
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL")

@app.get("/")
def root():
    return {"message": "✅ AI Calling Agent Live with Vonage!"}

@app.post("/webhooks/answer")
def answer_call():
    ncco = [
        {
            "action": "stream",
            "streamUrl": [f"{RENDER_BASE_URL}/static/desiree_response.mp3"]
        }
    ]
    return JSONResponse(content=ncco)

@app.post("/webhooks/event")
async def handle_event(request: Request):
    payload = await request.json()
    print("📞 Event Received:", payload)

    uuid = payload.get("uuid")
    speech = payload.get("speech", {}).get("text")  # If speech-to-text is sent
    dtmf = payload.get("dtmf", {}).get("digits")    # If keypad is used

    user_input = speech or dtmf or "..."

    from gpt_elevenlabs import generate_gpt_reply, generate_voice

    # Use GPT to continue the conversation
    next_prompt = f"The user said: '{user_input}'. What should I ask next in an insurance phone interview?"
    reply_text = generate_gpt_reply(next_prompt)

    # Save new audio response
    audio_path = f"static/response_{uuid}.mp3"
    generate_voice(reply_text, output_path=audio_path)

    print(f"✅ Generated reply: {reply_text}")
    print(f"🎧 MP3 saved to: {audio_path}")

    return {"status": "ok"}
from fastapi.responses import FileResponse

@app.get("/webhooks/next")
def serve_next(uuid: str):
    audio_path = f"static/response_{uuid}.mp3"
    if os.path.exists(audio_path):
        ncco = [
            {
                "action": "stream",
                "streamUrl": [f"{RENDER_BASE_URL}/webhooks/next-audio?uuid={uuid}"]
            }
        ]
        return JSONResponse(content=ncco)
    else:
        return JSONResponse(content={"error": "Response audio not ready."}, status_code=404)

@app.get("/webhooks/next-audio")
def stream_mp3(uuid: str):
    path = f"static/response_{uuid}.mp3"
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    return {"error": "File not found"}
