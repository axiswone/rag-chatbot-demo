from typing import Dict, Optional


def apply_profile_fallbacks(
    profile: Optional[Dict[str, str]] = None
) -> Dict[str, str]:

    if profile is None:

        profile = {}

    return {

        "user_role": profile.get(
            "user_role",
            "Developer"
        ),

        "user_preferences": profile.get(
            "user_preferences",
            "Concise, annotated responses"
        ),

        "user_activity": profile.get(
            "user_activity",
            "General troubleshooting"
        ),
    }