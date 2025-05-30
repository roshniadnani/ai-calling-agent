import os
import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path to the service account key
SERVICE_ACCOUNT_FILE = os.path.join("credentials", "ai_service_account.json")

# Google Sheet ID from .env
SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_ID")

# Sheet tab name (you confirmed it's "AI_Calling_Responses")
SHEET_NAME = "AI_Calling_Responses"

# Authenticate
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()

def write_row_to_sheet(data: list):
    """Appends a single row to the Google Sheet."""
    range_name = f"{SHEET_NAME}!A2"  # Appends below header row
    body = {
        "values": [data]
    }
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
    print("✅ Row written to Google Sheet:", result.get("updates", {}).get("updatedRange", "No update info"))

# Optional: test data row
def test_write_dummy_row():
    sample_data = [
        datetime.datetime.now().isoformat(),
        "+13023098006", "John Doe", "123 Main St", "New York", "10001",
        "1990-01-01", "1992-02-02", "john.doe@example.com", "Auto",
        "100000", "Toyota Corolla 2021", "Yes - Thursday 2 PM", "Needs inspection"
    ]
    write_row_to_sheet(sample_data)

# Uncomment below line to test
# test_write_dummy_row()
