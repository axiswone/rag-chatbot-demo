"""Helpers for embedding, storing, and retrieving semantic chat history."""

from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from typing import List, Tuple, Optional
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import CHAT_HISTORY_INDEX_PATH, EMBEDDING_MODEL_NAME
from app.models import ChatTurn

# Initialize embedding model and vector store with error handling
# The module-level store keeps the index warm so every request does not have to hit disk.
try:
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    if not os.path.exists(CHAT_HISTORY_INDEX_PATH):
        # Create empty index for first run
        chat_vectorstore = FAISS.from_texts(
            texts=["Initial empty index"],
            embedding=embedding_model,
            metadatas=[{"user_id": "system", "role": "system"}],
        )
        chat_vectorstore.save_local(CHAT_HISTORY_INDEX_PATH)
    else:
        chat_vectorstore = FAISS.load_local(
            CHAT_HISTORY_INDEX_PATH,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True,
        )
except Exception as e:
    raise RuntimeError(f"Failed to initialize chat history vector store: {str(e)}")


def retrieve_semantic_chat_history(
    user_query: str, user_id: str, k: int = 5, score_threshold: float = 0.7
) -> str:
    """
    Retrieve semantically relevant chat history for a given user query.

    Args:
        user_query: The query to find relevant history for
        user_id: The ID of the user to get history for
        k: Number of relevant messages to retrieve
        score_threshold: Minimum similarity score (0-1) for results

    Returns:
        A string containing the relevant chat history formatted as 'role: message'

    Raises:
        ValueError: If user_query is empty or k < 1
        RuntimeError: If FAISS search fails
    """
    if not user_query.strip():
        raise ValueError("user_query cannot be empty")
    if k < 1:
        raise ValueError("k must be at least 1")
    if not 0 <= score_threshold <= 1:
        raise ValueError("score_threshold must be between 0 and 1")

    try:
        results: List[Tuple[Document, float]] = (
            chat_vectorstore.similarity_search_with_score(user_query, k=k)
        )
        # Filter by user_id and similarity score
        # This keeps conversations siloed even if multiple users share the same backend.
        relevant_turns = [
            f"{r.metadata['role']}: {r.page_content}"
            for r, score in results
            if r.metadata["user_id"] == user_id and score >= score_threshold
        ]
        return "\n".join(relevant_turns)
    except Exception as e:
        raise RuntimeError(f"Failed to search chat history: {str(e)}")


def embed_and_store_chat_turn(turn: ChatTurn) -> None:
    """
    Embed and store a chat turn in the vector store.

    Args:
        turn: The ChatTurn model instance to store

    Raises:
        ValueError: If turn is None or has empty required fields
        RuntimeError: If storing in vector store fails
    """
    if not turn:
        raise ValueError("turn cannot be None")
    if not turn.message or not turn.message.strip():
        raise ValueError("turn.message cannot be empty")

    try:
        chat_vectorstore.add_texts(
            [turn.message],
            metadatas=[
                {
                    "user_id": turn.user_id,
                    "session_id": turn.session_id,
                    "role": turn.role.value if hasattr(turn.role, "value") else str(turn.role),
                    "timestamp": turn.timestamp.isoformat(),
                }
            ],
        )
        # Persist the index immediately so the Streamlit explorer can reflect the turn.
        chat_vectorstore.save_local(CHAT_HISTORY_INDEX_PATH)
    except Exception as e:
        raise RuntimeError(f"Failed to store chat turn: {str(e)}")
