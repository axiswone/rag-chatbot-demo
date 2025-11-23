"""Configuration loading and validation for backend paths and settings."""

import os
from typing import Final, Optional
from dotenv import load_dotenv
from pathlib import Path
from app.utils import logger


def _validate_path(path: str) -> str:
    """Ensure path exists and create if necessary."""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def _validate_int(name: str, value: str, min_val: int, max_val: int) -> int:
    """Validate and convert integer environment variables."""
    try:
        val = int(value)
        if not min_val <= val <= max_val:
            raise ValueError(f"{name} must be between {min_val} and {max_val}")
        return val
    except ValueError as e:
        logger.error(f"Invalid {name} value: {value}")
        raise ValueError(f"Invalid {name} value: {str(e)}")


# Get application root directory
APP_ROOT: Final[str] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load and validate environment variables
load_dotenv(dotenv_path=os.path.join(APP_ROOT, ".env"))

# Vector index paths with validation
# These directories hold the serialized FAISS stores that power retrieval.
DATA_ROOT: Final[str] = _validate_path(os.path.join(APP_ROOT, "data"))
DOCS_INDEX_PATH: Final[str] = _validate_path(os.path.join(DATA_ROOT, "docs_index"))
TICKETS_INDEX_PATH: Final[str] = os.path.abspath(
    os.path.join(DATA_ROOT, "tickets_index")
)
CONFIGS_INDEX_PATH: Final[str] = _validate_path(
    os.path.join(DATA_ROOT, "configs_index")
)
CHAT_HISTORY_INDEX_PATH: Final[str] = _validate_path(
    os.path.join(DATA_ROOT, "chat_history_index")
)

# Model settings with validation
# Keep the set of allowed models small so new learners do not accidentally
# point the code at an unsupported or expensive LLM.
VALID_LLM_MODELS = ["gpt-4", "gpt-3.5-turbo"]

LLM_MODEL_NAME: Final[str] = os.getenv("LLM_MODEL", "gpt-4")
if LLM_MODEL_NAME not in VALID_LLM_MODELS:
    raise ValueError(f"Invalid LLM_MODEL. Must be one of: {VALID_LLM_MODELS}")

# API key validation
# Beginners often forget to copy their key, so we fail fast with a clear message.
# Note: If using a free provider like Groq, you will need to set GROQ_API_KEY instead.
OPENAI_API_KEY: Final[str] = os.getenv("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")
if not OPENAI_API_KEY.startswith("sk-"):
    raise ValueError("Invalid OPENAI_API_KEY format")

# Retrieval settings with validation
# `TOP_K_RETRIEVAL` controls how many chunks come back from each vector store.
# Larger numbers increase recall but also cost more tokens when we call the LLM.
TOP_K_RETRIEVAL: Final[int] = _validate_int(
    "TOP_K_RETRIEVAL", os.getenv("TOP_K_RETRIEVAL", "3"), min_val=1, max_val=10
)

CHAT_HISTORY_LIMIT: Final[int] = _validate_int(
    "CHAT_HISTORY_LIMIT", os.getenv("CHAT_HISTORY_LIMIT", "5"), min_val=1, max_val=20
)

# Embedding model configuration
# Defaults to the free MiniLM model so the project runs without extra setup.
EMBEDDING_MODEL_NAME: Final[str] = os.getenv(
    "EMBEDDING_MODEL", "all-MiniLM-L6-v2"
)

# Default user profile fallbacks
# These values seed every new chat request so the experience is consistent
# even when the frontend does not provide explicit persona details.
DEFAULT_USER_ROLE: Final[str] = os.getenv("DEFAULT_USER_ROLE", "Developer")
DEFAULT_USER_PREFERENCES: Final[str] = os.getenv(
    "DEFAULT_USER_PREFERENCES", "Concise, annotated responses"
)
DEFAULT_USER_ACTIVITY: Final[str] = os.getenv(
    "DEFAULT_USER_ACTIVITY", "General troubleshooting"
)
