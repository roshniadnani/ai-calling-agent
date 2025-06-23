import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from gpt_elevenlabs import generate_voice

load_dotenv()

app = FastAPI()

session_state = {}

questions = [
    "Hi there! This is Desiree from FutureNet. Am I speaking with the right person?",
    "Awesome! Quick question – have you had a chance to look into our AI workflow tools?",
    "They’re built to save you tons of time on repetitive tasks. Would you like a quick demo link?",
    "Perfect, I’ll send that your way. Is this the best number to follow up?",
    "Great, thanks for your time. Talk soon!"
]

@app.get("/")
def root():
    return {"message": "Desiree AI Calling Agent is live."}

@app.get("/webhooks/answer")
def answer_call():
    greeting = questions[0]
    generate_voice(greeting, "static/desiree_response.mp3")
    return JSONResponse([
        {"action": "stream", "streamUrl": ["https://ai-calling-agent-9hv2.onrender.com/static/desiree_response.mp3"]}
    ])

@app.post("/webhooks/event")
async def handle_event(request: Request):
    data = await request.json()

    uuid = data.get("uuid") or data.get("conversation_uuid")
    if not uuid:
        return JSONResponse(status_code=400, content={"error": "Missing uuid"})

    state = session_state.setdefault(uuid, {"idx": 0, "answers": []})
    event_type = data.get("status") or data.get("speech", {}).get("timeout_reason", "")

    if data.get("speech", {}).get("text"):
        user_input = data["speech"]["text"]
        state["answers"].append(user_input)
        state["idx"] += 1

        if state["idx"] < len(questions):
            next_question = questions[state["idx"]]
            file_path = f"static/response_{state['idx']}.mp3"
            generate_voice(next_question, file_path)
            return JSONResponse([
                {"action": "stream", "streamUrl": [f"https://ai-calling-agent-9hv2.onrender.com/{file_path}"]}
            ])
        else:
            return JSONResponse([
                {"action": "talk", "text": "Thank you for your time. Goodbye!"}
            ])
    else:
        return JSONResponse([{"action": "listen", "eventUrl": ["https://ai-calling-agent-9hv2.onrender.com/webhooks/event"]}])
