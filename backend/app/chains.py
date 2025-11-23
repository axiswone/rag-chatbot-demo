"""
LangChain Chains and Agent Configuration

This module initializes the LangChain components for the RAG chatbot:
- MultiRetrievalQAChain: Used for RAG-based responses (currently active)

ARCHITECTURE OVERVIEW:
The system has one approach:
1. MultiRetrievalQAChain (ACTIVE): Retrieves context from vector stores and generates responses

MEMORY MANAGEMENT:
- Uses semantic memory (vector-based) for conversation context
- LangChain memory available but not used - semantic memory preferred
- Semantic memory provides better topic-based retrieval than sequential memory

CURRENT USAGE:
- main.py uses only the multi_retrieval_chain for chat responses
"""

from typing import List
from langchain_openai import ChatOpenAI
from langchain.chains import MultiRetrievalQAChain, ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate

# LangChain memory available but not used - semantic memory preferred
from langchain_community.vectorstores import FAISS
from langchain.schema import BaseRetriever
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import (
    DOCS_INDEX_PATH,
    TICKETS_INDEX_PATH,
    CONFIGS_INDEX_PATH,
    LLM_MODEL_NAME,
    TOP_K_RETRIEVAL,
)
import os
from app.utils import logger


def initialize_llm() -> ChatOpenAI:
    """Initialize the language model with error handling."""
    try:
        return ChatOpenAI(
            model_name=LLM_MODEL_NAME,
            temperature=0.7,  # Add some creativity while keeping responses focused
        )
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {str(e)}")
        raise RuntimeError("Failed to initialize language model")


def initialize_retrievers() -> List[BaseRetriever]:
    """Initialize FAISS retrievers with error handling."""
    try:
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        retrievers = []
        # Initialize each retriever with proper error handling
        for path, name in [
            (DOCS_INDEX_PATH, "docs"),
            (TICKETS_INDEX_PATH, "tickets"),
            (CONFIGS_INDEX_PATH, "configs"),
        ]:
            try:
                retriever = FAISS.load_local(
                    path, embeddings=embedding_model, allow_dangerous_deserialization=True
                ).as_retriever(search_kwargs={"k": TOP_K_RETRIEVAL})
                retrievers.append(retriever)
            except Exception as e:
                logger.error(f"Failed to load {name} retriever: {str(e)}")
                # Continue with available retrievers

        if not retrievers:
            raise RuntimeError("No retrievers could be initialized")
        return retrievers

    except Exception as e:
        logger.error(f"Failed to initialize retrievers: {str(e)}")
        raise RuntimeError("Failed to initialize retrieval system")


# =============================================================================
# COMPONENT INITIALIZATION
# =============================================================================
# Initialize all LangChain components with error handling

try:
    # Initialize LLM
    llm = initialize_llm()

    # Memory initialization available but not used - using semantic memory instead
    # LangChain ConversationBufferMemory could be used but semantic memory is preferred
    # Semantic memory provides better topic-based retrieval than sequential memory

    # Initialize prompt template for consistent response formatting
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant supporting {user_role}."),
            ("system", "User preferences: {user_preferences}"),
            ("system", "Recent activity: {user_activity}"),
            ("system", "Conversation so far:\n{chat_history}"),
            ("user", "{user_query}"),
        ]
    )

    # Initialize retrievers for vector search
    retrievers = initialize_retrievers()
    docs_retriever = retrievers[0]
    
    retriever_infos = [
        {
            "name": "docs",
            "description": "Good for answering questions about documentation",
            "retriever": retrievers[0],
        },
        {
            "name": "tickets",
            "description": "Good for answering questions about tickets",
            "retriever": retrievers[1],
        },
        {
            "name": "configs",
            "description": "Good for answering questions about configs",
            "retriever": retrievers[2],
        },
    ]
    # Note: this simple prototype assumes all three indexes are available.
    # If you remove one, adjust the retriever list accordingly.


    # =============================================================================
    # MULTI-RETRIEVAL CHAIN (CURRENTLY ACTIVE)
    # =============================================================================
    # This chain is used in main.py for RAG-based responses
    # It searches across multiple vector stores and generates responses
    # Get verbose setting from environment variable
    verbose_mode = os.getenv("VERBOSE_CHAINS", "false").lower() == "true"

    default_chain = ConversationalRetrievalChain.from_llm(llm, docs_retriever, prompt=prompt)

    multi_retrieval_chain = MultiRetrievalQAChain.from_retrievers(
        llm=llm,
        retriever_infos=retriever_infos,
        default_chain=default_chain,
        verbose=verbose_mode
    )

except Exception as e:
    logger.error(f"Failed to initialize chain components: {str(e)}")
    raise RuntimeError("Failed to initialize chat system")
