import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# ✅ Load JSON string from Render Environment Variable
service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])
credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

# ✅ Use .env or Render secret to set these
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "AI_Calling_Responses")

def append_row_to_sheet(data: list):
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp] + data

    request = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": [row]}
    )
    request.execute()
