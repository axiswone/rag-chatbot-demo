"""FastAPI entrypoint for the RAG chatbot API and supporting workflows."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from app.models import ChatTurn, RoleType
from app.chat_history import embed_and_store_chat_turn, retrieve_semantic_chat_history
from app.utils import apply_profile_fallbacks, log_interaction, generate_session_id, logger
from app.config import (
    DOCS_INDEX_PATH,
    TICKETS_INDEX_PATH,
    CONFIGS_INDEX_PATH,
    TOP_K_RETRIEVAL,
    CHAT_HISTORY_LIMIT,
    CHAT_HISTORY_INDEX_PATH,
    EMBEDDING_MODEL_NAME,
    DEFAULT_USER_ROLE,
    DEFAULT_USER_PREFERENCES,
    DEFAULT_USER_ACTIVITY,
)

from langchain_openai import ChatOpenAI
from langchain.chains import MultiRetrievalQAChain, LLMChain
from langchain.prompts import ChatPromptTemplate

# LangChain memory available but not used - semantic memory preferred
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# Request/Response models
class ChatRequest(BaseModel):
    user_query: str = Field(..., min_length=1, max_length=1000)
    user_id: str = Field(default="anonymous", max_length=50)
    session_id: Optional[str] = Field(default=None, max_length=36)
    user_role: str = Field(default=DEFAULT_USER_ROLE)
    user_preferences: str = Field(default=DEFAULT_USER_PREFERENCES)
    user_activity: str = Field(default=DEFAULT_USER_ACTIVITY)


class ChatResponse(BaseModel):
    response: str


# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="A chatbot using Retrieval-Augmented Generation for contextual responses",
    version="0.1.0",
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For prototype only - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components with error handling
try:
    # Use a free, local embedding model from Hugging Face
    # Sticking to the same embeddings across every store keeps similarity scores comparable.
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    tickets_top_k = max(TOP_K_RETRIEVAL, 8)

    # Load retrievers with specific error handling for missing files
    try:
        docs_retriever = FAISS.load_local(
            DOCS_INDEX_PATH, embeddings=embedding_model, allow_dangerous_deserialization=True
        ).as_retriever(search_kwargs={"k": max(TOP_K_RETRIEVAL, 6)})
    except Exception as e:
        raise RuntimeError(
            f"Failed to load docs index from {DOCS_INDEX_PATH}. Run 'python scripts/generate_indexes.py' to create indexes."
        )

    try:
        tickets_retriever = FAISS.load_local(
            TICKETS_INDEX_PATH, embeddings=embedding_model, allow_dangerous_deserialization=True
        ).as_retriever(search_kwargs={"k": tickets_top_k})
    except Exception as e:
        raise RuntimeError(
            f"Failed to load tickets index from {TICKETS_INDEX_PATH}. Run 'python scripts/generate_indexes.py' to create indexes."
        )

    try:
        configs_retriever = FAISS.load_local(
            CONFIGS_INDEX_PATH, embeddings=embedding_model, allow_dangerous_deserialization=True
        ).as_retriever(search_kwargs={"k": TOP_K_RETRIEVAL})
    except Exception as e:
        raise RuntimeError(
            f"Failed to load configs index from {CONFIGS_INDEX_PATH}. Run 'python scripts/generate_indexes.py' to create indexes."
        )

    try:
        chat_vectorstore = FAISS.load_local(
            CHAT_HISTORY_INDEX_PATH,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True,
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to load chat history index from {CHAT_HISTORY_INDEX_PATH}. Run 'python scripts/generate_indexes.py' to create indexes."
        )

except Exception as e:
    raise RuntimeError(f"Failed to initialize RAG components: {str(e)}")

# Load LLM
# Note: LangChain memory (ConversationBufferMemory) is available but not used
# This system uses semantic memory (vector-based) for conversation context instead
# Semantic memory provides better topic-based retrieval than sequential memory

# By default, this uses OpenAI. To switch to a free model, see the options below.
# Feel free to swap this out while you experiment; the rest of the pipeline is model-agnostic.
llm = ChatOpenAI()

# =============================================================================
# OPTION 1: USE A FREE HOSTED MODEL (e.g., Groq)
# =============================================================================
# 1. Add `langchain-groq` to requirements.txt and `pip install -r backend/requirements.txt`
# 2. Get a free API key from https://console.groq.com/
# 3. Set `GROQ_API_KEY` in your backend/.env file
# 4. Comment out `llm = ChatOpenAI()` above and uncomment the following lines:
#
# from langchain_groq import ChatGroq
# llm = ChatGroq(model_name="llama3-8b-8192")
# =============================================================================

# =============================================================================
# OPTION 2: USE A FREE LOCAL MODEL (e.g., Ollama)
# =============================================================================
# 1. Add `langchain-ollama` to requirements.txt and `pip install -r backend/requirements.txt`
# 2. Install Ollama from https://ollama.com and run `ollama pull llama3:8b`
# 3. Comment out `llm = ChatOpenAI()` above and uncomment the following lines:
#
# from langchain_community.chat_models import ChatOllama
# llm = ChatOllama(model="llama3:8b")
# =============================================================================

retrieval_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a helpful assistant answering questions using the retrieved knowledge base.\n"
                "Always ground your responses in the provided Context. If the context lists multiple items "
                "(for example, several tickets), reason over each entry before answering. When the user asks "
                "for tickets by status, list every matching ticket ID along with its status and other relevant fields.\n"
                "If the necessary information is not present in the context, explicitly say so."
            ),
        ),
        (
            "human",
            "Context:\n{context}\n\nQuestion:\n{question}",
        ),
    ]
)
# Default/fallback chain only gets a single formatted `input`, so give it a matching prompt.
fallback_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant grounded in provided persona details and prior chat history.",
        ),
        ("human", "{query}"),
    ]
)

retriever_infos = [
    {
        "name": "docs",
        "description": "Good for answering questions about documentation",
        "retriever": docs_retriever,
        "prompt": retrieval_prompt,
    },
    {
        "name": "tickets",
        "description": "Good for answering questions about tickets",
        "retriever": tickets_retriever,
        "prompt": retrieval_prompt,
    },
    {
        "name": "configs",
        "description": "Good for answering questions about configs",
        "retriever": configs_retriever,
        "prompt": retrieval_prompt,
    },
]

default_chain = LLMChain(llm=llm, prompt=fallback_prompt, output_key="result")

multi_chain = MultiRetrievalQAChain.from_retrievers(
    llm=llm,
    retriever_infos=retriever_infos,
    default_chain=default_chain,
)
logger.info("Multi-retrieval chain input keys: %s", multi_chain.input_keys)


@app.post(
    "/chat", response_model=ChatResponse, summary="Get a response from the chatbot"
)
async def chat(request: ChatRequest):
    """
    Get a response from the chatbot based on user query and context.

    - Uses RAG to provide relevant responses
    - Maintains chat history in vector store
    - Personalizes based on user profile
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or generate_session_id()

        # Retrieve chat history from vector store using semantic memory
        # This replaces traditional sequential memory with topic-based retrieval
        # Finds relevant conversation history regardless of recency
        chat_history = retrieve_semantic_chat_history(
            request.user_query, request.user_id, k=CHAT_HISTORY_LIMIT
        )

        # =============================================================================
        # RAG-BASED RESPONSE GENERATION (CURRENTLY ACTIVE)
        # =============================================================================
        # This uses MultiRetrievalQAChain to search vector stores and generate responses
        # The chain searches across docs, tickets, and configs for relevant context
        # Build a single string that carries persona, recent history, and the actual question.
        formatted_query = (
            f"User role: {request.user_role}\n"
            f"User preferences: {request.user_preferences}\n"
            f"Recent activity: {request.user_activity}\n"
            f"Prior chat context:\n{chat_history or 'None'}\n"
            f"Question: {request.user_query}"
        )
        chain_inputs = {"input": formatted_query}
        result = multi_chain.invoke(chain_inputs)
        response = result.get("result") if isinstance(result, dict) else result
        if not response:
            response = "I'm sorry, I couldn't generate a response with the available context."

        # Store user turn in vector store for semantic memory
        # Each turn is embedded and stored for future topic-based retrieval
        embed_and_store_chat_turn(
            turn=ChatTurn(
                user_id=request.user_id,
                session_id=session_id,
                role=RoleType.USER,
                message=request.user_query,
            )
        )

        # Store assistant turn in vector store for semantic memory
        # Both user and assistant turns are stored to maintain conversation context
        embed_and_store_chat_turn(
            turn=ChatTurn(
                user_id=request.user_id,
                session_id=session_id,
                role=RoleType.ASSISTANT,
                message=response,
            )
        )

        # Log interaction
        log_interaction(request.user_id, request.user_query, response)

        return ChatResponse(response=response)

    except Exception as e:
        # Log the error but don't expose internal details
        log_interaction(request.user_id, request.user_query, f"Error: {str(e)}")
        logger.exception("Chat handler failed")
        raise HTTPException(
            status_code=500, detail="An error occurred while processing your request"
        )
