from fastapi import APIRouter, HTTPException
from app.models import UserProfile

router = APIRouter()

fake_db = {}

@router.post("/save_profile")
async def save_user_profile(profile: UserProfile):
    fake_db[profile.user_id] = profile
    return {
        "message": "Profile saved successfully.",
        "profile": profile
    }

@router.get("/get_profile/{user_id}")
async def get_user_profile(user_id: str):
    profile = fake_db.get(user_id)
    if profile:
        return {"profile": profile}
    raise HTTPException(status_code=404, detail="Profile not found")

@router.get("/match/{user_id}")
async def get_matches(user_id: str):
    user_profile = fake_db.get(user_id)
    if not user_profile:
        return {"error": "User profile not found."}

    matches = []
    for uid, other in fake_db.items():
        if uid == user_id:
            continue

        score = sum([
            user_profile.personality_type == other.personality_type,
            user_profile.attachment_style == other.attachment_style,
            user_profile.love_language == other.love_language,
            user_profile.relationship_goals == other.relationship_goals
        ])
        matches.append({
            "user_id": uid,
            "match_score": score,
            "overlap_traits": score / 4.0
        })

    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return {"matches": matches}
