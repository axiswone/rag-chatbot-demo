"""Data models and enums describing chat turns exchanged with the API."""

import enum
from typing import Optional
from datetime import datetime


class RoleType(str, enum.Enum):
    """Enumerates who produced a message so we can filter chat history later."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatTurn:
    """
    Simple data class for chat turns stored in vector store.
    Not a database model - used for structuring data before vectorization.
    """

    def __init__(
        self,
        user_id: str,
        session_id: str,
        role: RoleType,
        message: str,
        timestamp: Optional[datetime] = None,
    ):
        if not user_id or len(user_id) > 50:
            raise ValueError("user_id cannot be empty or longer than 50 chars")
        if not message or not message.strip():
            raise ValueError("message cannot be empty")

        self.user_id = user_id
        self.session_id = session_id
        # `role` is used as metadata in FAISS; keep the raw enum for readability.
        self.role = role
        self.message = message.strip()
        self.timestamp = timestamp or datetime.utcnow()

    def __repr__(self) -> str:
        return f"<ChatTurn(user_id={self.user_id}, role={self.role}, message={self.message[:30]}...)>"
