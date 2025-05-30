import vonage

# Vonage credentials
VONAGE_API_KEY = "4071bee6"
VONAGE_API_SECRET = "8Hl3J5qPprZUCoCG"
VONAGE_APPLICATION_ID = "0f4f9a52-9da7-4372-8117-dc04674315c7"
VONAGE_VIRTUAL_NUMBER = "+12028772945"  # Replace with your actual Vonage virtual number
TO_NUMBER = "+13023098006"  # Destination number to call

# Load private key file for JWT auth
client = vonage.Client(
    application_id=VONAGE_APPLICATION_ID,
    private_key="private.key"
)
voice = vonage.Voice(client)

# Initiate the outbound call
response = voice.create_call({
    "to": [{"type": "phone", "number": TO_NUMBER}],
    "from": {"type": "phone", "number": VONAGE_VIRTUAL_NUMBER},
    "ncco": [
        {
            "action": "talk",
            "text": "Hello, this is Desiree from Homesite. I will now begin the survey. Please hold on.",
            "voiceName": "Amy"  # Can change to ElevenLabs streaming later
        }
    ]
})

print("Vonage call initiated. Response:")
print(response)
