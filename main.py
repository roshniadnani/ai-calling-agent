from fastapi import FastAPI, Request
from call_vonage import make_call
from gpt_elevenlabs import generate_gpt_reply, generate_voice

app = FastAPI()


@app.get("/")
def root():
    return {"message": "AI Calling Agent is running."}


@app.get("/make-call/{to_number}")
def call_user(to_number: str):
    print(f"TO NUMBER SENT: {to_number}")
    make_call(to_number)
    return {"status": "Call initiated", "number": to_number}


@app.post("/webhooks/answer")
async def answer_call(request: Request):
    from fastapi.responses import JSONResponse

    request_data = await request.json()
    print("Vonage Answer Webhook:", request_data)

    # Simulated first line to start call
    gpt_text = generate_gpt_reply("")
    audio_url = generate_voice(gpt_text)

    ncco = [
        {
            "action": "stream",
            "streamUrl": [audio_url]
        }
    ]
    return JSONResponse(content=ncco)


@app.post("/webhooks/event")
async def handle_event(request: Request):
    event_data = await request.json()
    print("Vonage Event Webhook:", event_data)
    return {"status": "received"}
