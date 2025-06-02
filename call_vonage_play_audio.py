import vonage
import os

# Load private key correctly as PEM content
with open("private.key", "r") as f:
    private_key = f.read()

client = vonage.Client(
    application_id="0f4f9a52-9da7-4372-8117-dc04674315c7",  # Your App ID
    private_key=private_key
)
voice = vonage.Voice(client)

to_number = input("Enter the phone number to call (e.g., +1234567890): ")

response = voice.create_call({
    "to": [{"type": "phone", "number": to_number}],
    "from": {"type": "phone", "number": "+12405963842"},
    "answer_url": ["https://ai-calling-agent-9hv2.onrender.com/vonage-audio"]
})

print("Call started, response:")
print(response)
