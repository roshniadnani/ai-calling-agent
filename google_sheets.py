import json
import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "AI_Calling_Responses")

def get_sheet():
    # Load credentials from local JSON file
    SERVICE_ACCOUNT_FILE = "C:/Users/sc/Desktop/ai_calling_agent/ai-calling-agent-461408-f3080ffc6b7f.json"
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    return sheet

def append_row_to_sheet(row_data):
    try:
        sheet = get_sheet()
        sheet.append_row(row_data, value_input_option="RAW")
        print("✅ Data appended to Google Sheet.")
    except Exception as e:
        print(f"❌ Error appending to sheet: {e}")
