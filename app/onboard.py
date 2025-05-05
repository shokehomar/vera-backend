from fastapi import APIRouter
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from app.profile import fake_db  # Import your in-memory DB
from app.models import Message, ConversationPayload, UserProfile

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

@router.post("/chat")
async def onboard_chat(payload: ConversationPayload):
    system_prompt = {
    "role": "system",
    "content": (
        "You are VERA, a warm, thoughtful AI dating coach who talks like a real person, not a script. "
        "Your goal is to build rapport during onboarding and understand the user’s relationship mindset. "
        "Use natural, casual language. Be curious and kind — ask a question only if it feels natural. "
        "Reflect on what the user says. Avoid sounding like an interview. You can share your thoughts, too, in a playful way."
    )
}


    if payload.profile:
        profile_description = (
            f"\n\nThe user is a {payload.profile.personality_type} with a "
            f"{payload.profile.attachment_style} attachment style, prefers "
            f"{payload.profile.love_language}, and is looking for a "
            f"{payload.profile.relationship_goals} relationship."
        )
        system_prompt["content"] += profile_description

    try:
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



@router.post("/extract_profile")
async def extract_profile(payload: ConversationPayload):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an emotionally intelligent assistant trained in relationship psychology. "
                        "Based on the user's conversation, infer the following profile traits:\n"
                        "- personality_type (MBTI-style: e.g. ENTP, INFP, etc.)\n"
                        "- attachment_style (secure, anxious, avoidant, etc.)\n"
                        "- love_language (e.g. words of affirmation, quality time, etc.)\n"
                        "- relationship_goals (casual, serious, long-term, exploring, etc.)\n\n"
                        "Respond ONLY in valid JSON like:\n"
                        "{\n"
                        "  \"personality_type\": \"ENTP\",\n"
                        "  \"attachment_style\": \"secure\",\n"
                        "  \"love_language\": \"quality time\",\n"
                        "  \"relationship_goals\": \"serious\"\n"
                        "}"
                        "Only ask 5-10 questions before extracting the profile."
                    )
                }
            ] + [msg.model_dump() for msg in payload.conversation],
            temperature=0.5,
            max_tokens=300,
        )

        raw_output = response.choices[0].message.content
        parsed = json.loads(raw_output)

        if not payload.user_id:
            return {"error": "user_id required in payload to save profile"}

        # Build and save the UserProfile
        profile = UserProfile(user_id=payload.user_id, **parsed)
        fake_db[payload.user_id] = profile

        return {
            "message": "Profile extracted and saved.",
            "extracted_profile": profile
        }

    except Exception as e:
        return {"error": str(e)}