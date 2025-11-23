"""Command-line utility to rebuild the documentation FAISS index.

NOTE: Run from backend/scripts (or via Streamlit) so relative paths resolve correctly.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import DOCS_INDEX_PATH
from pathlib import Path
import textwrap

CHUNK_SIZE = 800  # characters per chunk; simple heuristic that keeps Markdown headings intact
CHUNK_OVERLAP = 200  # small overlap so a heading sentence is not lost between two chunks

def load_docs_from_files() -> list:
    """Load documentation from data/docs/ directory"""
    docs_path = Path("../data/docs")
    if not docs_path.exists():
        raise FileNotFoundError(
            "No documentation found in data/docs/. "
            "Run 'python ../data-generators/generate_sample_data.py' to create sample data."
        )
    
    docs = []
    metadatas = []
    
    for file_path in docs_path.glob("**/*"):
        if file_path.is_file() and file_path.suffix in ['.md', '.txt', '.rst']:
            try:
                content = file_path.read_text(encoding='utf-8')
                if not content.strip():
                    continue

                # Chunk the document to improve retrieval granularity
                cleaned = content.replace("\r\n", "\n").strip()
                # `textwrap.wrap` operates on characters, which is sufficient for this teaching project.
                tokens = list(textwrap.wrap(cleaned, CHUNK_SIZE, drop_whitespace=False))

                for idx, chunk in enumerate(tokens):
                    # Extend the chunk with overlap from the previous section when possible
                    if idx > 0 and CHUNK_OVERLAP > 0:
                        overlap = cleaned[max(0, (idx * CHUNK_SIZE) - CHUNK_OVERLAP): idx * CHUNK_SIZE]
                        chunk = overlap + chunk

                    chunk = chunk.strip()
                    if not chunk:
                        continue

                    docs.append(chunk)
                    metadatas.append({
                        "source": "docs",
                        "file": str(file_path),
                        "topic": file_path.stem,
                        "chunk": idx,
                    })
            except Exception as e:
                print(f"  Warning: Could not read {file_path}: {e}")
                continue
    
    if not docs:
        raise ValueError("No documentation files found in data/docs/")
    
    return docs, metadatas

if __name__ == "__main__":
    # This allows the script to be run standalone
    from index_utils import generate_index
    generate_index(DOCS_INDEX_PATH, load_docs_from_files, "documents")
