from __future__ import annotations
from pydantic import BaseModel
from typing import List, Literal, Optional

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class UserProfile(BaseModel):
    user_id: str
    personality_type: str
    attachment_style: str
    love_language: str
    relationship_goals: str

class ConversationPayload(BaseModel):
    user_id: Optional[str] = None
    conversation: List[Message]
    profile: Optional[UserProfile] = None

