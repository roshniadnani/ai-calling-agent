from fastapi import FastAPI
from gpt_elevenlabs import generate_gpt_reply, generate_voice
from pydub import AudioSegment
from pydub.playback import play
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🎙️ AI Calling Agent is running!"}

@app.get("/call")
def initiate_call():
    try:
        # Step 1: Generate GPT Interview Script
        gpt_text = generate_gpt_reply()
        print("📝 GPT Output:\n", gpt_text)

        # Step 2: Generate MP3 Audio from Desiree Voice Agent
        mp3_path = generate_voice(gpt_text)
        print(f"✅ MP3 saved as {mp3_path}")

        # Step 3: Return the audio file as HTTP response
        return FileResponse(mp3_path, media_type="audio/mpeg", filename="desiree_output.mp3")

    except Exception as e:
        print("❌ Error:", str(e))
        return {"error": str(e)}
