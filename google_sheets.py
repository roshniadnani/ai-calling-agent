import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Define the required Google Sheets API scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# ✅ Use environment variable on Render, or fallback to local file when running locally
if "GOOGLE_SERVICE_ACCOUNT" in os.environ:
    service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])
    credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
else:
    credentials = Credentials.from_service_account_file(
        "credentials/ai-calling-agent-461408-f3080ffc6b7f.json", scopes=SCOPES
    )

# ✅ Sheet ID and Sheet Name from environment variables
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "AI_Calling_Responses")

def append_row_to_sheet(data: list):
    """
    Appends a single row of data to the configured Google Sheet.
    """
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
