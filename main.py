from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import vonage
import os

app = FastAPI()

# Load credentials
VONAGE_APPLICATION_ID = os.getenv("VONAGE_APPLICATION_ID")
PRIVATE_KEY_PATH = "private.key"  # Ensure this file exists and is formatted correctly

# Create Vonage client using PEM-formatted private key
client = vonage.Client(
    application_id=VONAGE_APPLICATION_ID,
    private_key=open(PRIVATE_KEY_PATH, "r").read()
)
voice = vonage.Voice(client)

@app.get("/")
async def root():
    return {"message": "Your service is live 🎉"}

@app.post("/call")
async def trigger_outbound_call(request: Request):
    try:
        body = await request.json()
        to_number = body.get("to")
        if not to_number:
            return JSONResponse(status_code=400, content={"error": "Missing 'to' number"})

        print(f"📞 Initiating outbound call to: {to_number}")

        response = voice.create_call({
            "to": [{"type": "phone", "number": to_number}],
            "from": {"type": "phone", "number": os.getenv("VONAGE_NUMBER")},
            "ncco": [{
                "action": "talk",
                "text": "Hello! This is a test call from your AI calling agent."
            }]
        })

        print("🔹 Vonage Response:", response)
        return response

    except Exception as e:
        print("❌ Error during outbound call:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
