from vonage import Voice
import os
from dotenv import load_dotenv

load_dotenv()

voice = Voice(
    application_id=os.getenv("VONAGE_APPLICATION_ID"),
    private_key=os.getenv("VONAGE_PRIVATE_KEY")
)

response = voice.create_call({
    "to": [{"type": "phone", "number": "+13104211169"}],
    "from": {"type": "phone", "number": os.getenv("VONAGE_VIRTUAL_NUMBER")},
    "answer_url": [f"{os.getenv('RENDER_BASE_URL')}/answer"],
    "event_url": [f"{os.getenv('RENDER_BASE_URL')}/event"]
})
print(response)
