import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import vonage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Environment credentials
VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_APPLICATION_ID = os.getenv("VONAGE_APPLICATION_ID")
VONAGE_PRIVATE_KEY_PATH = os.getenv("VONAGE_PRIVATE_KEY_PATH")
VONAGE_VIRTUAL_NUMBER = os.getenv("VONAGE_VIRTUAL_NUMBER")
BASE_URL = os.getenv("BASE_URL")

# Initialize Vonage client (corrected)
client = vonage.Client(
    application_id=VONAGE_APPLICATION_ID,
    private_key=VONAGE_PRIVATE_KEY_PATH,
    key=VONAGE_API_KEY,
    secret=VONAGE_API_SECRET
)
voice = client.voice

@app.get("/")
def home():
    return {"message": "AI Calling Agent is Live."}

@app.get("/make-call/{number}")
def make_call(number: str):
    response = voice.create_call({
        "to": [{"type": "phone", "number": number}],
        "from": {"type": "phone", "number": VONAGE_VIRTUAL_NUMBER},
        "ncco": [
            {
                "action": "stream",
                "streamUrl": [f"{BASE_URL}/static/desiree_response.mp3"]
            }
        ]
    })
    return response
