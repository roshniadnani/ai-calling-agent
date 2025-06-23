import os
import json
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "AI_Calling_Responses")

def get_sheet():
    try:
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        with open(credentials_path, "r") as file:
            service_account_info = json.load(file)
        credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
        return sheet
    except Exception as e:
        print(f"❌ Failed to access Google Sheet: {e}")
        return None

def append_row_to_sheet(row_data):
    sheet = get_sheet()
    if sheet:
        try:
            final_row = row_data[:15]  # Align with 15 expected columns
            final_row += [""] * (15 - len(final_row))  # Pad with blanks if fewer entries
            sheet.append_row(final_row, value_input_option="RAW")
            print("✅ Data appended to Google Sheet.")
        except Exception as e:
            print(f"❌ Error appending to sheet: {e}")
