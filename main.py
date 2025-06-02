from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
import os
from google_sheets import append_row_to_sheet
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class CallData(BaseModel):
    caller_number: str
    name: str = ""
    address: str = ""
    city: str = ""
    zip_code: str = ""
    dob: str = ""
    spouse_dob: str = ""
    email: str = ""
    policy_type: str = ""
    coverage_amount: str = ""
    vehicle_info: str = ""
    appointment_scheduled: str = ""
    notes: str = ""

@app.get("/")
async def root():
    return {"message": "AI Calling Agent is running."}

@app.post("/log-to-sheet")
async def log_to_sheet(data: CallData):
    try:
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.caller_number,
            data.name,
            data.address,
            data.city,
            data.zip_code,
            data.dob,
            data.spouse_dob,
            data.email,
            data.policy_type,
            data.coverage_amount,
            data.vehicle_info,
            data.appointment_scheduled,
            data.notes
        ]
        append_row_to_sheet(row)
        return {"status": "success", "message": "Data logged to sheet."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
