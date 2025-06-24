import os
import json
import gspread
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "AI_Calling_Responses")
CRED_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def get_sheet():
    if not CRED_PATH or not SHEET_ID:
        raise EnvironmentError("❌ Missing GOOGLE_APPLICATION_CREDENTIALS or SHEET_ID in .env")

    try:
        with open(CRED_PATH, "r") as f:
            service_account_info = json.load(f)
        credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
        print(f"✅ Connected to Sheet: '{SHEET_NAME}' (ID: {SHEET_ID})")
        return sheet
    except Exception as e:
        print(f"❌ Google Sheets access failed: {e}")
        return None

def append_row_to_sheet(row_data):
    sheet = get_sheet()
    if sheet:
        try:
            headers = sheet.row_values(1)
            if not headers:
                print("⚠️ Sheet is empty—using default column size.")
                num_cols = 15
            else:
                num_cols = len(headers)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_row = [timestamp] + row_data
            padded_row = full_row + [""] * (num_cols - len(full_row))

            print("🧾 Sheet headers:", headers)
            print("📌 Row being added:", padded_row[:num_cols])

            sheet.append_row(padded_row[:num_cols], value_input_option="RAW")
            print("✅ Row with timestamp added to Google Sheet.")
        except Exception as e:
            print(f"❌ Couldn't append row: {e}")
