# Matchmaking logic (refined)
from fastapi import APIRouter
from app.models import UserProfile

router = APIRouter()

# Placeholder for real DB
fake_db = {}

def score_match(user: UserProfile, candidate: UserProfile) -> int:
    score = 0

    # Attachment style match
    if user.attachment_style == candidate.attachment_style:
        score += 2

    # Personality type match (simple rule for now)
    if user.personality_type[0] == candidate.personality_type[0]:  # E/I match
        score += 1

    # Love language match
    if user.love_language == candidate.love_language:
        score += 2
    elif user.love_language in candidate.love_language:
        score += 1  # loose match (multi-preference)

    # Relationship goals match
    if user.relationship_goals == candidate.relationship_goals:
        score += 3

    return score

@router.post("/match")
async def find_matches(target_user: UserProfile, pool: list[UserProfile]):
    matches = []

    for candidate in pool:
        if candidate.user_id == target_user.user_id:
            continue  # don't match with self

        match_score = score_match(target_user, candidate)

        if match_score >= 5:  # Threshold for a "good" match
            matches.append({
                "user_id": candidate.user_id,
                "personality_type": candidate.personality_type,
                "attachment_style": candidate.attachment_style,
                "love_language": candidate.love_language,
                "relationship_goals": candidate.relationship_goals,
                "match_score": match_score
            })

    matches.sort(key=lambda x: x["match_score"], reverse=True)

    return {
        "target_user": target_user.user_id,
        "matches_found": len(matches),
        "matches": matches
    }
