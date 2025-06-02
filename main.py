# main.py

import subprocess
import sys

# ⛑️ Emergency install: Fixes Render bug where installed module is not found
try:
    import vonage
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "vonage==2.6.0"])
    import vonage

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "✅ AI Calling Agent Live with Vonage!"}
