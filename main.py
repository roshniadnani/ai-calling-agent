import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from vonage_call import initiate_call

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Vonage AI Calling Agent is live!"}

@app.post("/webhook/answer")
async def answer_call(request: Request):
    return {
        "actions": [
            {
                "action": "talk",
                "voiceName": "Amy",
                "text": "Hello! This is your Vonage AI calling agent. Thank you for answering the call."
            }
        ]
    }

@app.post("/webhook/event")
async def call_event(request: Request):
    payload = await request.json()
    print("Call event received:", payload)
    return {"status": "ok"}

@app.get("/make-call")
def make_call():
    response = initiate_call()
    return {"response": response}
