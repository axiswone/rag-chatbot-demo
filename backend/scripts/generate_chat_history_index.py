"""Command-line utility to regenerate the chat history FAISS index.

NOTE: Run from backend/scripts (or via Streamlit) so relative paths resolve correctly.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import CHAT_HISTORY_INDEX_PATH
from pathlib import Path
import json

def load_chat_history_from_files() -> list:
    """Load chat history from data/chat_history/ directory"""
    chat_path = Path("../data/chat_history")
    if not chat_path.exists():
        raise FileNotFoundError(
            "No chat history found in data/chat_history/. "
            "Run 'python ../data-generators/generate_sample_data.py' to create sample data."
        )
    
    texts = []
    metadatas = []
    
    for file_path in chat_path.glob("**/*"):
        if file_path.is_file() and file_path.suffix in ['.json', '.txt', '.csv']:
            try:
                if file_path.suffix == '.json':
                    # Load JSON chat data
                    with open(file_path, 'r', encoding='utf-8') as f:
                        chat_data = json.load(f)
                    
                    # Extract messages from conversation
                    messages = chat_data.get('messages', [])
                    for msg in messages:
                        role = msg.get('role', 'unknown')
                        message = msg.get('message', '')
                        
                        if message.strip():
                            texts.append(message)
                            metadatas.append({
                                "role": role,
                                "user_id": chat_data.get('user_id', 'unknown'),
                                "session_id": chat_data.get('session_id', ''),
                                "file": str(file_path),
                                "timestamp": chat_data.get('timestamp', '')
                            })
                else:
                    # Load plain text files (assume format: "role: message")
                    content = file_path.read_text(encoding='utf-8')
                    if content.strip():
                        texts.append(content)
                        metadatas.append({
                            "role": "unknown",
                            "user_id": "unknown",
                            "file": str(file_path)
                        })
            except Exception as e:
                print(f"  Warning: Could not read {file_path}: {e}")
                continue
    
    if not texts:
        raise ValueError("No chat history files found in data/chat_history/")
    
    return texts, metadatas

if __name__ == "__main__":
    # This allows the script to be run standalone
    from index_utils import generate_index
    generate_index(CHAT_HISTORY_INDEX_PATH, load_chat_history_from_files, "chat messages")
