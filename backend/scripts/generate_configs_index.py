"""Command-line utility to rebuild the configuration documents FAISS index.

NOTE: Run from backend/scripts (or via Streamlit) so relative paths resolve correctly.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from index_utils import generate_index
from app.config import CONFIGS_INDEX_PATH
from pathlib import Path
import json

def load_configs_from_files() -> list:
    """Load configuration files from data/configs/ directory"""
    configs_path = Path("../data/configs")
    if not configs_path.exists():
        raise FileNotFoundError(
            "No configuration files found in data/configs/. "
            "Run 'python ../data-generators/generate_sample_data.py' to create sample data."
        )
    
    configs = []
    metadatas = []
    
    for file_path in configs_path.glob("**/*"):
        if file_path.is_file() and file_path.suffix in ['.yaml', '.yml', '.json', '.ini', '.conf', '.cfg']:
            try:
                content = file_path.read_text(encoding='utf-8')
                if content.strip():  # Only add non-empty files
                    configs.append(content)
                    metadatas.append({
                        "source": "configs",
                        "file": str(file_path),
                        "format": file_path.suffix[1:],  # Remove the dot
                        "name": file_path.stem
                    })
            except Exception as e:
                print(f"  Warning: Could not read {file_path}: {e}")
                continue
    
    if not configs:
        raise ValueError("No configuration files found in data/configs/")
    
    return configs, metadatas

if __name__ == "__main__":
    # This allows the script to be run standalone
    generate_index(CONFIGS_INDEX_PATH, load_configs_from_files, "configuration files")
