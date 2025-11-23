"""Command-line utility to rebuild the support tickets FAISS index.

NOTE: Run from backend/scripts (or via Streamlit) so relative paths resolve correctly.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import TICKETS_INDEX_PATH

from pathlib import Path
import json

def load_tickets_from_files() -> list:
    """Load support tickets from data/tickets/ directory"""
    tickets_path = Path("../data/tickets")
    if not tickets_path.exists():
        raise FileNotFoundError(
            "No support tickets found in data/tickets/. "
            "Run 'python ../data-generators/generate_sample_data.py' to create sample data."
        )
    
    tickets = []
    metadatas = []
    
    for file_path in tickets_path.glob("**/*"):
        if file_path.is_file() and file_path.suffix in ['.json', '.txt', '.csv']:
            try:
                if file_path.suffix == '.json':
                    # Load JSON ticket data
                    with open(file_path, 'r', encoding='utf-8') as f:
                        ticket_data = json.load(f)
                    
                    # Extract relevant information for indexing
                    title = ticket_data.get('title', '')
                    description = ticket_data.get('description', '')
                    severity = ticket_data.get('severity', 'unknown')
                    
                    ticket_id = ticket_data.get("id", "")
                    status = ticket_data.get("status", "unknown")
                    priority = ticket_data.get("priority", "unknown")
                    assignee = ticket_data.get("assignee", "unassigned")

                    # Combine structured fields for better retrieval
                    content = (
                        f"Ticket ID: {ticket_id}\n"
                        f"Status: {status}\n"
                        f"Severity: {severity}\n"
                        f"Priority: {priority}\n"
                        f"Assignee: {assignee}\n"
                        f"Title: {title}\n"
                        f"Description: {description}"
                    )

                    if content.strip():
                        tickets.append(content)
                        metadatas.append({
                            "source": "tickets",
                            "file": str(file_path),
                            "severity": severity,
                            "id": ticket_id,
                            "status": status,
                            "priority": priority,
                            "assignee": assignee,
                            # Rich metadata lets the LLM cite ticket details
                            # without having to extract the fields from free-form text.
                        })
                else:
                    # Load plain text files
                    content = file_path.read_text(encoding='utf-8')
                    if content.strip():
                        tickets.append(content)
                        metadatas.append({
                            "source": "tickets",
                            "file": str(file_path),
                            "severity": "unknown"
                        })
            except Exception as e:
                print(f"  Warning: Could not read {file_path}: {e}")
                continue
    
    if not tickets:
        raise ValueError("No support ticket files found in data/tickets/")
    
    return tickets, metadatas

if __name__ == "__main__":
    # This allows the script to be run standalone
    from index_utils import generate_index
    generate_index(TICKETS_INDEX_PATH, load_tickets_from_files, "support tickets")
