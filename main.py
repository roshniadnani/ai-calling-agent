# main.py
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
from pathlib import Path
import vonage

load_dotenv()

app = FastAPI()

client = vonage.Client(
    application_id=os.getenv("VONAGE_APPLICATION_ID"),
    private_key=Path("private.key").read_text()
)
voice = vonage.Voice(client)

@app.get("/")
def root():
    return {"message": "AI Calling Agent is live"}

@app.post("/webhook/answer")
async def answer_call(request: Request):
    return {
        "actions": [
            {"action": "talk", "text": "Hello, this is Desiree. Let's begin the call."}
        ]
    }

@app.post("/webhook/event")
async def event_handler(request: Request):
    return {"status": "received"}
