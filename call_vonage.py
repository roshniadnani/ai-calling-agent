import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

# ✅ LIVE Render URL for Vonage to stream from
RENDER_BASE_URL = "https://ai-calling-agent-9hv2.onrender.com"

@router.get("/webhooks/answer")
async def answer_call():
    """
    Respond to Vonage with an NCCO: stream Desiree's voice, then listen for input.
    """
    audio_url = f"{RENDER_BASE_URL}/static/desiree_response.mp3"

    ncco = [
        {
            "action": "stream",
            "streamUrl": [audio_url]
        },
        {
            "action": "input",
            "eventUrl": [f"{RENDER_BASE_URL}/webhooks/event"],
            "speech": {
                "language": "en-US",
                "endOnSilence": 1,
                "maxDuration": 5
            },
            "dtmf": {
                "maxDigits": 1,
                "timeOut": 5
            }
        }
    ]

    print(f"📡 NCCO sent: Streaming {audio_url} then listening for input")
    return JSONResponse(content=ncco)
