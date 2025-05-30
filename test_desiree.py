from gpt_elevenlabs import generate_gpt_reply, generate_voice

prompt = "What is your full name?"
reply = generate_gpt_reply(prompt)
audio_path = generate_voice(reply)

print(f"Voice saved to: {audio_path}")
