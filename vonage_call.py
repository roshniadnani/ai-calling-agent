import vonage
import os
from dotenv import load_dotenv

load_dotenv()

VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_APPLICATION_ID = os.getenv("VONAGE_APPLICATION_ID")
VONAGE_VIRTUAL_NUMBER = os.getenv("VONAGE_VIRTUAL_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER", VONAGE_VIRTUAL_NUMBER)  # default to own number for demo

# Path to the private.key file
private_key_path = os.path.join(os.path.dirname(__file__), "private.key")

client = vonage.Client(
    application_id=VONAGE_APPLICATION_ID,
    private_key=private_key_path
)

voice = vonage.Voice(client)

def initiate_call():
    response = voice.create_call({
        "to": [{"type": "phone", "number": TO_NUMBER}],
        "from": {"type": "phone", "number": VONAGE_VIRTUAL_NUMBER},
        "answer_url": [os.getenv("RENDER_BASE_URL") + "/webhook/answer"]
    })
    print("Vonage response:", response)
    return response
