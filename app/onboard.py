from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Literal
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define FastAPI router
router = APIRouter()

# Pydantic models
class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ConversationPayload(BaseModel):
    conversation: List[Message]

# Route for onboarding chat
@router.post("/chat")
async def onboard_chat(payload: ConversationPayload):
    system_prompt = {
        "role": "system",
        "content": (
            "You are VERA, a warm, thoughtful AI dating coach. "
            "Your job is to get to know users during onboarding, understand their relationship goals, tone, and emotional preferences. "
            "Ask meaningful, open-ended questions. Always be curious, empathetic, and a little playful when appropriate."
        )
    }

    try:
        # Create a chat completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[system_prompt] + [msg.model_dump() for msg in payload.conversation],
            temperature=0.7,
            max_tokens=200,
        )

        reply = response.choices[0].message.content
        return {"response": reply}

    except Exception as e:
        return {"error": str(e)}
