import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Insurance script questions
INSURANCE_QUESTIONS = [
    "Can I speak with the primary policyholder, please?",
    "My name is Desiree from Millennium. I'm calling to complete your phone interview for your recent insurance inquiry. Is now a good time?",
    "To begin, may I please confirm the address you’re looking to insure?",
    "Great, what type of property is this? (Single-family, duplex, condo, etc.)",
    "Is this property your primary residence, a secondary home, or a rental?",
    "Do you currently have insurance on this property?",
    "Have you filed any claims in the last 5 years?",
    "What’s the estimated year the home was built?",
    "Is there a central heating system?",
    "Has the roof been replaced in the past 10 years?",
    "Are there any pets, pools, or trampolines on the property?",
    "Would you like us to send you a calendar link to schedule the next step with a licensed agent?"
]

# Generate next GPT-4 response based on index and previous context
def get_next_prompt(index: int, previous_answers: list):
    if index < len(INSURANCE_QUESTIONS):
        return INSURANCE_QUESTIONS[index]
    else:
        return "Thank you! That concludes the interview. An agent will reach out shortly."

def get_ai_response(user_input: str, idx: int, history: list):
    prompt = f"""You are Desiree, an intelligent, friendly, and efficient insurance assistant.
You are guiding a user through a scripted phone interview and logging answers step-by-step.
You only ask one question at a time, wait for the answer, then continue.

The script so far:
{chr(10).join(f"Q{i+1}: {INSURANCE_QUESTIONS[i]}\nA{i+1}: {a}" for i, a in enumerate(history))}

Now ask the next question in a clear, polite tone:"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Desiree, a virtual agent for insurance interviews."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        reply = completion.choices[0].message['content'].strip()
        return reply
    except Exception as e:
        print(f"❌ GPT API Error: {e}")
        return get_next_prompt(idx, history)
