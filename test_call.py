import os
from dotenv import load_dotenv
from vonage import Voice

load_dotenv()

# Load private key from file
private_key_path = os.getenv("VONAGE_PRIVATE_KEY_PATH")
with open(private_key_path, "r") as f:
    private_key = f.read()

# Setup Vonage
voice = Voice(
    application_id=os.getenv("VONAGE_APPLICATION_ID"),
    private_key=private_key
)

# Trigger a call
to_number = "+13104211169"  # Replace with test number
print(f"📞 Initiating outbound call to: {to_number}")

try:
    response = voice.create_call({
        "to": [{"type": "phone", "number": to_number}],
        "from": {"type": "phone", "number": os.getenv("VONAGE_VIRTUAL_NUMBER")},
        "answer_url": [f"{os.getenv('RENDER_BASE_URL')}/answer"],
        "event_url": [f"{os.getenv('RENDER_BASE_URL')}/event"]
    })
    print("✅ Call created successfully.")
    print("🔹 Response:", response)
except Exception as e:
    print("❌ Error during outbound call:")
    print(e)
