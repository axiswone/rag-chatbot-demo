"""CLI helper that rebuilds every FAISS index used by the chatbot.

NOTE: Run from backend/scripts (or via Streamlit) so relative paths resolve correctly.
"""

import os
import sys

# Ensure the scripts directory is on the Python path
sys.path.append(os.path.dirname(__file__))

# Import the shared utility and the specific data loaders
from index_utils import generate_index
from generate_docs_index import load_docs_from_files
from generate_tickets_index import load_tickets_from_files
from generate_configs_index import load_configs_from_files
from generate_chat_history_index import load_chat_history_from_files

# Import configuration paths
from app.config import (
    DOCS_INDEX_PATH, TICKETS_INDEX_PATH, CONFIGS_INDEX_PATH, CHAT_HISTORY_INDEX_PATH
)

def main():
    """
    Runs all data indexing scripts sequentially.
    """
    print("Generating all FAISS indexes for demo...")
    
    # Keep track of each individual run so we can surface partial failures.
    results = []
    results.append(generate_index(DOCS_INDEX_PATH, load_docs_from_files, "documents"))
    results.append(generate_index(TICKETS_INDEX_PATH, load_tickets_from_files, "support tickets"))
    results.append(generate_index(CONFIGS_INDEX_PATH, load_configs_from_files, "configuration files"))
    results.append(generate_index(CHAT_HISTORY_INDEX_PATH, load_chat_history_from_files, "chat messages"))
    
    if all(results):
        print("\nAll indexes generated successfully.")
    else:
        print("\nSome indexes could not be generated. Please check the logs for errors.")

if __name__ == "__main__":
    main()
