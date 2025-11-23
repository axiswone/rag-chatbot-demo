"""Logging utilities, session helpers, and profile fallbacks for the service."""

import logging
from uuid import uuid4
from typing import Dict, Optional
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

# Always write logs to the repo-level logs/ folder regardless of cwd.
REPO_ROOT = Path(__file__).resolve().parents[2]
log_dir = REPO_ROOT / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("chat_logger")
handler = RotatingFileHandler(
    log_dir / "chat.log", maxBytes=10_000_000, backupCount=3  # 10MB
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def apply_profile_fallbacks(profile: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Apply fallback values for missing profile fields.

    Args:
        profile: Dictionary containing user profile data.
               If None, returns default values for all fields.

    Returns:
        Dictionary with all required profile fields, using defaults where needed.
    """
    if profile is None:
        profile = {}

    return {
        "user_role": profile.get("user_role", "Developer"),
        "user_preferences": profile.get(
            "user_preferences", "Concise, annotated responses"
        ),
        "user_activity": profile.get("user_activity", "General troubleshooting"),
    }


def log_interaction(user_id: str, query: str, response: str) -> None:
    """
    Log a chat interaction with proper sanitization.

    Args:
        user_id: The ID of the user making the query
        query: The user's query text
        response: The system's response text
    """
    try:
        # Sanitize inputs to prevent log injection
        safe_user_id = user_id.replace("\n", "").replace("\r", "")[:50]
        safe_query = query.replace("\n", " ").replace("\r", " ")[:500]
        safe_response = response.replace("\n", " ").replace("\r", " ")[:500]

        logger.info(f"[{safe_user_id}] Query: {safe_query}")
        logger.info(f"[{safe_user_id}] Response: {safe_response}")
    except Exception as e:
        logger.error(f"Failed to log interaction: {str(e)}")


def generate_session_id() -> str:
    """
    Generate a new unique session ID.

    Returns:
        A string containing a UUID4 for use as a session identifier.
    """
    return str(uuid4())
