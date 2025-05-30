import vonage
import os
from dotenv import load_dotenv

load_dotenv()

client = vonage.Client(
    application_id=os.getenv("VONAGE_APPLICATION_ID"),
    private_key=open(os.getenv("VONAGE_PRIVATE_KEY_PATH")).read()
)
voice = vonage.Voice(client)

response = voice.create_call({
    "to": [{"type": "phone", "number": "<YOUR_PHONE_NUMBER>"}],
    "from": {"type": "phone", "number": "+12405963842"},
    "ncco": [
        {
            "action": "talk",
            "text": "Hello, this is Desiree, your AI assistant. Welcome!"
        }
    ]
})

print(response)
