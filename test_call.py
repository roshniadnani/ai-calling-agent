import os
import traceback
from dotenv import load_dotenv
from vonage import Voice

# Load environment variables from .env file
load_dotenv()

# Read the private key from file
private_key_path = os.getenv("VONAGE_PRIVATE_KEY_PATH")
print(f"🔐 PRIVATE_KEY_PATH: {private_key_path}")

with open(private_key_path, "r") as f:
    private_key = f.read()

print(f"🔑 Private Key Loaded (First 30 chars): {private_key[:30]}")

# Initialize Vonage Voice client
voice = Voice(
    application_id=os.getenv("VONAGE_APPLICATION_ID"),
    private_key=private_key
)

# Prepare call parameters
to_number = "+13104211169"  # Replace with desired test number
from_number = os.getenv("VONAGE_VIRTUAL_NUMBER")
answer_url = f"{os.getenv('RENDER_BASE_URL')}/answer"
event_url = f"{os.getenv('RENDER_BASE_URL')}/event"

print(f"📞 Initiating outbound call to: {to_number}")
print(f"📤 From: {from_number}")
print(f"🌐 Answer URL: {answer_url}")
print(f"📈 Event URL: {event_url}")

# Trigger the call
try:
    response = voice.create_call({
        "to": [{"type": "phone", "number": to_number}],
        "from": {"type": "phone", "number": from_number},
        "answer_url": [answer_url],
        "event_url": [event_url]
    })
    print("✅ Call created successfully.")
    print("🔹 Response:", response)
except Exception as e:
    print("❌ Exception occurred during outbound call:")
    print(e)
    traceback.print_exc()
