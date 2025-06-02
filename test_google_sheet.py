from google_sheets import append_row_to_sheet
from datetime import datetime

# Dummy test data matching your sheet headers
test_data = [
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
    "+11234567890",  # Caller Number
    "John Doe",      # Name
    "123 Main St",   # Address
    "New York",      # City
    "10001",         # Zip Code
    "1990-01-01",    # DOB
    "1992-02-02",    # Spouse DOB
    "john@example.com",  # Email
    "Auto",          # Policy Type
    "$100,000",      # Coverage Amount
    "2020 Toyota Camry", # Vehicle Info
    "Yes",           # Appointment Scheduled
    "Test entry"     # Notes
]

append_row_to_sheet(test_data)
print("✅ Row appended successfully to Google Sheet!")
