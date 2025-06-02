import json
import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "AI_Calling_Responses")  # Optional fallback

def get_sheet():
    # Load Render secret containing the full JSON key
    service_account_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT"))
    credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
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
