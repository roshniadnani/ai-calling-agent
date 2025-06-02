import os
import gspread
from google.oauth2.service_account import Credentials

# Path to the service account key JSON file in the 'credentials' folder
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "credentials", "ai-calling-agent-461408-f3080ffc6b7f.json")

# Define the scope for accessing Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]


# Create credentials and authorize gspread client
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)

# Open the spreadsheet and the first worksheet
spreadsheet = gc.open("AI_Calling_Responses")
worksheet = spreadsheet.sheet1

def append_row_to_sheet(row_data):
    """
    Appends a new row of data to the Google Sheet.
    :param row_data: List of values matching the header order.
    """
    worksheet.append_row(row_data, value_input_option="USER_ENTERED")
