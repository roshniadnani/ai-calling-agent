# --- Force install vonage if missing ---
try:
    import vonage
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "vonage==2.6.0"])
    import vonage

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

load_dotenv()

VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_VIRTUAL_NUMBER = os.getenv("VONAGE_VIRTUAL_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")

client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
voice = vonage.Voice(client)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Calling Agent is live."}

@app.get("/call")
def make_call():
    response = voice.create_call({
        "to": [{"type": "phone", "number": TO_NUMBER}],
        "from": {"type": "phone", "number": VONAGE_VIRTUAL_NUMBER},
        "ncco": [{
            "action": "talk",
            "text": "Hello, this is Desiree from Millennium Information Services. This is a test call from your AI assistant."
        }]
    })
    return JSONResponse(content=response)

@app.post("/webhooks/answer")
async def answer_call(request: Request):
    return JSONResponse(content=[{
        "action": "talk",
        "text": "Hi, this is Desiree. Thanks for picking up the call. I will now proceed with the phone interview."
    }])

@app.post("/webhooks/event")
async def event_callback(request: Request):
    event_data = await request.json()
    print("Vonage Event:", event_data)
    return JSONResponse(content={"status": "received"})
