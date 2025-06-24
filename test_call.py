import os
from dotenv import load_dotenv
from vonage import Voice

# Load environment variables from .env file
load_dotenv()

# Read the private key from file path
private_key_path = os.getenv("VONAGE_PRIVATE_KEY_PATH")
print("🔐 PRIVATE_KEY_PATH:", private_key_path)

try:
    with open(private_key_path, "r") as f:
        private_key = f.read()
    print("🔑 Private Key Loaded (First 30 chars):", private_key[:30], "...")
except Exception as e:
    print("❌ Error loading private key:", e)
    exit()

# Initialize Vonage Voice client
try:
    voice = Voice(
        application_id=os.getenv("VONAGE_APPLICATION_ID"),
        private_key=private_key
    )
except Exception as e:
    print("❌ Error initializing Vonage client:", e)
    exit()

# Trigger an outbound call
to_number = "+13104211169"  # Replace with test number
from_number = os.getenv("VONAGE_VIRTUAL_NUMBER")
answer_url = f"{os.getenv('RENDER_BASE_URL')}/answer"
event_url = f"{os.getenv('RENDER_BASE_URL')}/event"

print("📞 Initiating outbound call to:", to_number)
print("📤 From:", from_number)
print("🌐 Answer URL:", answer_url)
print("📈 Event URL:", event_url)

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
    print("❌ Error during outbound call:")
    print(e)
