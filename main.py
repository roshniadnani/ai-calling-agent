from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from google_sheets import append_row_to_sheet
from datetime import datetime

load_dotenv()

app = FastAPI()

# Optional CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "✅ AI Calling Agent is running."}

# Test writing to Google Sheet
@app.get("/test-sheet")
async def test_sheet():
    test_data = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "+11234567890",
        "John Doe",
        "123 Main St",
        "New York",
        "10001",
        "1990-01-01",
        "1992-02-02",
        "john@example.com",
        "Auto",
        "$100,000",
        "2020 Toyota Camry",
        "Yes",
        "Test entry"
    ]
    append_row_to_sheet(test_data)
    return {"status": "✅ Row added to Google Sheet"}

# Vonage-compatible endpoint to stream Desiree's voice
@app.get("/vonage-desiree-audio")
async def vonage_desiree_audio():
    return {
        "actions": [
            {
                "action": "stream",
                "streamUrl": [f"{os.getenv('RENDER_URL')}/static/desiree_response.mp3"]
            }
        ]
    }
