import requests

# Function to generate speech using ElevenLabs API
def generate_speech(text, voice_id="zWRDoH56JB9twPHdkksW", api_key="sk_eb35891891b639b2337526f9dae63157abdf3257be9118b0"):
    url = "https://api.elevenlabs.io/v1/text-to-speech/generate"
    
    # Define the headers for the request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Define the data payload with text and voice ID
    data = {
        "text": text,  # The text you want to convert to speech
        "voice": voice_id  # Desiree's voice ID (replace with your voice ID)
    }

    # Make the API request to generate speech
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        # If successful, save the response content (audio) to a file
        audio_file_path = "output_audio.wav"  # This will be the generated audio file
        with open(audio_file_path, "wb") as f:
            f.write(response.content)
        print(f"Audio generated and saved at: {audio_file_path}")
        return audio_file_path  # Return the path of the generated audio file
    else:
        print(f"Error generating speech: {response.json()}")
        return None

# Example usage to generate speech (you can replace this text with anything you need for your call)
if __name__ == "__main__":
    text_to_speak = "Hello, this is Desiree calling. Can you confirm if the smoke detectors in your home are working?"
    audio_file_path = generate_speech(text_to_speak)  # Replace with the text you need
    if audio_file_path:
        print(f"Audio file generated successfully at {audio_file_path}")
