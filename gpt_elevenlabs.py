from elevenlabs import Voice, VoiceSettings, play, save, generate, set_api_key
import os

# ✅ Set ElevenLabs API Key
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

# ✅ Desiree voice ID (from ElevenLabs studio)
DESIREE_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Replace if you have custom ID

def generate_voice(text, filename="static/desiree_response.mp3"):
    try:
        audio = generate(
            text=text,
            voice=Voice(
                voice_id=DESIREE_VOICE_ID,
                settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.8,
                    style=0.3,
                    use_speaker_boost=True,
                ),
            )
        )
        save(audio, filename)
        print(f"✅ Audio saved to {filename}")
    except Exception as e:
        print(f"❌ Error generating voice: {e}")
