"""Shared helper functions for loading data and constructing FAISS indexes.

NOTE: This module is imported by scripts that assume they run from backend/scripts.
"""

import os
import sys
from pathlib import Path

# Ensure the app directory is on the Python path
sys.path.append(str(Path(__file__).parent.parent))

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.utils import logger

def generate_index(index_path: str, loader_fn, description: str) -> bool:
    """
    Generates and saves a FAISS index from loaded data.

    Args:
        index_path (str): The path to save the FAISS index.
        loader_fn (function): A function that loads documents and metadatas.
        description (str): A description of the data being indexed.
    
    Returns:
        bool: True if the index was generated successfully, False otherwise.
    """
    logger.info(f"Generating FAISS index for {description}...")

    try:
        # Load documents and metadata
        docs, metadatas = loader_fn()
        # Each loader returns one text chunk per entry along with optional metadata.
        logger.info(f"Found {len(docs)} {description} to index.")

        # Initialize embeddings
        logger.info("Initializing Hugging Face embeddings...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Create FAISS index
        logger.info("Creating FAISS index...")
        index = FAISS.from_texts(
            texts=docs,
            embedding=embeddings,
            metadatas=metadatas
        )

        # Save the index
        index.save_local(index_path)
        logger.info(f"FAISS index for {description} generated successfully at {index_path}")
        return True

    except FileNotFoundError as e:
        logger.error(f"Could not generate index for {description}: {e}")
        return False
    except ValueError as e:
        logger.error(f"Could not generate index for {description}: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred while generating the {description} index: {e}")
        return False
