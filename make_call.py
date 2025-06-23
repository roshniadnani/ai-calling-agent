import vonage
import os

def make_vonage_call(to_number):
    client = vonage.Client(
        key=os.getenv("VONAGE_API_KEY"),
        secret=os.getenv("VONAGE_API_SECRET")
    )
    voice = vonage.Voice(client)

    response = voice.create_call({
        "to": [{"type": "phone", "number": to_number}],
        "from": {"type": "phone", "number": os.getenv("VONAGE_VIRTUAL_NUMBER")},
        "answer_url": [os.getenv("ANSWER_URL")]
    })

    return response
