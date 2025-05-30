# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import vonage
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = vonage.Client(
    application_id=os.getenv("VONAGE_APPLICATION_ID"),
    private_key=open(os.getenv("VONAGE_PRIVATE_KEY_PATH")).read()
)
voice = vonage.Voice(client)

@app.get("/")
def root():
    return {"message": "AI Calling Agent is live!"}

@app.post("/webhook/answer")
async def answer_call(request: Request):
    return JSONResponse([
        {
            "action": "talk",
            "text": "Hello! This is Desiree, your AI assistant. How can I help you today?"
        }
    ])

@app.post("/webhook/event")
async def event_hook(request: Request):
    body = await request.body()
    print("Event:", body.decode())
    return JSONResponse({"status": "received"})
