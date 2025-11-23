"""Streamlit dashboard exposing chat, data generation, and data management tools."""

import os
import json
import shutil
import subprocess
from pathlib import Path
import sys
from typing import Dict, List, Optional, Set, Tuple
from uuid import uuid4

import requests
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

st.set_page_config(page_title="RAG Chatbot Prototype", layout="wide")

SIDEBAR_CSS = """
<style>
section[data-testid="stSidebar"] {
    min-width: 220px !important;
    max-width: 220px !important;
}
</style>
"""

# Resolve paths once; every callback reuses these constants.
FRONTEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = FRONTEND_DIR.parent
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
DATA_DIR = PROJECT_ROOT / "backend" / "data"
GENERATORS_DIR = PROJECT_ROOT / "data-generators"
GEN_SCRIPT = GENERATORS_DIR / "generate_sample_data.py"
INDEX_SCRIPT = PROJECT_ROOT / "backend" / "scripts" / "generate_indexes.py"
CHAT_HISTORY_INDEX_PATH = DATA_DIR / "chat_history_index"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

DOMAIN_OPTIONS = ["tech", "healthcare", "finance", "ecommerce", "general"]
VOLUME_OPTIONS = ["small", "medium", "large"]
COMPLEXITY_OPTIONS = ["basic", "intermediate", "advanced"]
DATA_BUCKETS = ["docs", "tickets", "configs", "chat_history"]
DEFAULT_USER_IDS = ["streamlit_user"]


def check_backend_health() -> Tuple[bool, str]:
    """Ping the FastAPI server to display a simple status badge."""
    try:
        response = requests.get(f"{BACKEND_URL}/docs", timeout=3)
        if response.status_code == 200:
            return True, "Online"
        return False, "Offline"
    except requests.RequestException:
        return False, "Offline"


def run_command(command: List[str], cwd: Path, env: Dict[str, str]) -> Tuple[bool, str]:
    """Run a subprocess command and return success flag plus combined output."""
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
        stdout = completed.stdout.strip()
        return True, stdout if stdout else "Command completed successfully."
    except subprocess.CalledProcessError as exc:
        output = "\n".join(filter(None, [exc.stdout, exc.stderr])).strip()
        message = output if output else str(exc)
        return False, message


def ensure_bucket(bucket: str) -> Path:
    """Ensure the target data bucket exists and return its path."""
    bucket_path = DATA_DIR / bucket
    bucket_path.mkdir(parents=True, exist_ok=True)
    return bucket_path


def list_bucket_contents(bucket: str) -> List[Dict[str, str]]:
    """Return metadata for files in the selected data bucket."""
    bucket_path = ensure_bucket(bucket)
    rows: List[Dict[str, str]] = []
    for item in sorted(bucket_path.iterdir()):
        if item.is_file():
            rows.append(
                {
                    "name": item.name,
                    "size_kb": f"{item.stat().st_size / 1024:.1f}",
                    "updated": item.stat().st_mtime_ns,
                }
            )
    return rows


def clear_sample_data(remove_indexes: bool = False) -> int:
    """Remove generated sample data from all buckets; return item count removed."""
    removed = 0
    for bucket in DATA_BUCKETS:
        bucket_path = DATA_DIR / bucket
        if not bucket_path.exists():
            continue
        for item in list(bucket_path.iterdir()):
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                removed += 1
            except OSError:
                pass
    if remove_indexes:
        index_paths = [
            DATA_DIR / "docs_index",
            DATA_DIR / "tickets_index",
            DATA_DIR / "configs_index",
            DATA_DIR / "chat_history_index",
        ]
        for index_path in index_paths:
            if index_path.exists():
                try:
                    shutil.rmtree(index_path)
                    removed += 1
                except OSError:
                    pass
    return removed


def get_chat_history_messages() -> Dict[str, List[Dict[str, Optional[str]]]]:
    """Load user messages stored in the FAISS chat history index."""
    if not CHAT_HISTORY_INDEX_PATH.exists():
        return {}

    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vectorstore = FAISS.load_local(
            str(CHAT_HISTORY_INDEX_PATH),
            embeddings=embeddings,
            allow_dangerous_deserialization=True,
        )
    except Exception:
        return {}

    history: Dict[str, List[Dict[str, Optional[str]]]] = {}
    # Streamlit only shows learner prompts, so filter out assistant/system turns.
    for doc in vectorstore.docstore._dict.values():
        metadata = getattr(doc, "metadata", {}) or {}
        role = str(metadata.get("role", "")).lower()
        if "user" not in role:
            continue
        user_id = metadata.get("user_id")
        if not isinstance(user_id, str) or not user_id.strip():
            continue
        history.setdefault(user_id.strip(), []).append(
            {
                "message": doc.page_content,
                "timestamp": metadata.get("timestamp"),
            }
        )

    for messages in history.values():
        messages.sort(key=lambda entry: entry.get("timestamp") or "", reverse=True)
    return history


def discover_user_ids() -> List[str]:
    """Surface known user IDs from chat history files."""
    user_ids: Set[str] = set(DEFAULT_USER_IDS)
    chat_history_dir = DATA_DIR / "chat_history"
    if chat_history_dir.exists():
        for item in chat_history_dir.glob("*.json"):
            try:
                with item.open("r", encoding="utf-8") as handle:
                    payload = json.load(handle)
                user_id = payload.get("user_id")
                if isinstance(user_id, str) and user_id.strip():
                    user_ids.add(user_id.strip())
            except (json.JSONDecodeError, OSError):
                continue

    # Include any additional personas saved in the vector store
    for user_id in get_chat_history_messages().keys():
        if user_id:
            user_ids.add(user_id)

    return sorted(user_ids)


def summarize_user_history(user_id: str) -> str:
    """Build a short summary of stored chat history for the chosen user."""
    history = get_chat_history_messages().get(user_id, [])
    if not history:
        return "No stored history for this user yet. Start chatting to build one."

    total_turns = len(history)
    samples = [entry["message"] for entry in history[:3]]
    sample_preview = "; ".join(
        f'"{snippet[:80]}{"..." if len(snippet) > 80 else ""}"' for snippet in samples
    )
    sentences = [
        f"Found {total_turns} prior user message(s) stored for `{user_id}`.",
    ]
    sentences.append(f"Recent prompts include: {sample_preview}.")
    return " ".join(sentences)


def render_sidebar() -> None:
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    st.sidebar.title("RAG Chatbot Demo")
    healthy, status_message = check_backend_health()
    status_icon = "🟢" if healthy else "🔴"
    status_label = "ONLINE" if healthy else "OFFLINE"
    st.sidebar.markdown(f"**Backend:** {status_icon} {status_label}")
    if not healthy:
        st.sidebar.markdown("---")
        st.sidebar.write("Start the FastAPI backend to enable chat and data actions.")
        st.sidebar.code("python -m uvicorn --app-dir backend app.main:app --reload")
        st.sidebar.write("Once the server is running, press the button below.")
        if st.sidebar.button("Retry connection"):
            st.rerun()


def handle_chat_tab() -> None:
    st.header("Chat with the RAG Assistant")
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid4())
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    user_options = discover_user_ids()
    if "user_id" not in st.session_state or st.session_state.user_id not in user_options:
        st.session_state.user_id = user_options[0]

    user_index = user_options.index(st.session_state.user_id)
    selected_user = st.selectbox(
        "Active user ID",
        user_options,
        index=user_index,
        help="Choose which user's memory should seed retrieval.",
    )
    if selected_user != st.session_state.user_id:
        st.session_state.user_id = selected_user
        st.session_state.chat_history = []
        st.session_state.session_id = str(uuid4())
        st.info(f"Switched to user '{selected_user}'. Session reset for this persona.")

    summary_text = summarize_user_history(st.session_state.user_id)
    st.caption(summary_text)

    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])

    prompt = st.chat_input("Ask a question about your knowledge base...")
    if prompt:
        # Update the streamlit transcript first so the user sees their message immediately.
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                payload = {
                    "user_query": prompt,
                    "user_id": st.session_state.user_id,
                    "session_id": st.session_state.session_id,
                }
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json=payload,
                    timeout=60,
                )
                if response.ok:
                    data = response.json()
                    answer = data.get("response", "No response received.")
                    st.markdown(answer)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )
                else:
                    st.error(f"Request failed: {response.status_code}")
            except requests.RequestException as exc:
                st.error(f"Unable to reach backend: {exc}")

    if st.button("Start New Session"):
        st.session_state.chat_history = []
        st.session_state.session_id = str(uuid4())
        st.success(
            f"Started a fresh session for user '{st.session_state.user_id}'. Conversation history cleared."
        )


def handle_generate_tab() -> None:
    st.header("Generate Synthetic Data")
    st.write("Adjust the configuration and trigger the generator script.")

    domain = st.selectbox("Domain", DOMAIN_OPTIONS)
    volume = st.selectbox("Volume", VOLUME_OPTIONS, index=1)
    complexity = st.selectbox("Complexity", COMPLEXITY_OPTIONS, index=1)

    col1, col2 = st.columns([1, 1])
    with col1:
        run_button = st.button("Generate Data", use_container_width=True)
    with col2:
        retain_existing = st.checkbox(
            "Retain existing domain data",
            value=True,
            help="Uncheck to purge existing domain files and indexes before generating.",
        )

    if run_button:
        if not retain_existing:
            removed = clear_sample_data(remove_indexes=True)
            st.warning(
                f"Cleared {removed} existing items and indexes before generating new data."
            )
        with st.spinner("Running data generator..."):
            env = os.environ.copy()
            env.update(
                {
                    "DATA_DOMAIN": domain,
                    "DATA_VOLUME": volume,
                    "DATA_COMPLEXITY": complexity,
                }
            )
            success, output = run_command([sys.executable, str(GEN_SCRIPT.name)], GENERATORS_DIR, env)
        if success:
            st.success("Synthetic data generated successfully.")
        else:
            st.error("Data generation failed. Review the logs below.")
        st.code(output or "No output captured.")

        if success:
            with st.spinner("Regenerating FAISS indexes..."):
                success_idx, output_idx = run_command(
                    [sys.executable, str(INDEX_SCRIPT.name)],
                    INDEX_SCRIPT.parent,
                    os.environ.copy(),
                )
            if success_idx:
                st.success("Indexes rebuilt successfully.")
            else:
                st.error("Index regeneration failed. See details below.")
            st.code(output_idx or "No output captured from index script.")

        if success and success_idx:
            st.info("Data generation complete. Reloading chat user list...")
            st.rerun()


def handle_upload_tab() -> None:
    st.header("Upload and Explore Data")
    st.info(
        "If you plan to rely solely on your own files, clear the bundled sample data before uploading."
    )

    if "management_mode" not in st.session_state:
        st.session_state.management_mode = "explore"

    col_a, col_b, col_c = st.columns(3)
    if col_a.button("Explore Files"):
        st.session_state.management_mode = "explore"
    if col_b.button("Upload Files"):
        st.session_state.management_mode = "upload"
    if col_c.button("Clear Sample Data"):
        st.session_state.management_mode = "clear"

    mode = st.session_state.management_mode

    if mode == "upload":
        bucket = st.selectbox("Target folder", DATA_BUCKETS, index=0)
        uploads = st.file_uploader(
            "Select files to upload",
            accept_multiple_files=True,
        )
        if uploads:
            bucket_path = ensure_bucket(bucket)
            saved_files: List[str] = []
            for uploaded_file in uploads:
                destination = bucket_path / uploaded_file.name
                with destination.open("wb") as handle:
                    handle.write(uploaded_file.getbuffer())
                saved_files.append(uploaded_file.name)
            st.success(f"Uploaded {len(saved_files)} file(s) to {bucket}.")
            st.write("Uploaded files:")
            st.write(saved_files)

            # Rebuild every index right away so the new files are searchable without manual steps.
            with st.spinner("Regenerating FAISS indexes..."):
                success_idx, output_idx = run_command(
                    [sys.executable, str(INDEX_SCRIPT.name)],
                    INDEX_SCRIPT.parent,
                    os.environ.copy(),
                )
            st.code(output_idx or "No output captured from index script.")
            if success_idx:
                st.success("Indexes rebuilt successfully.")
                st.info("Indexes updated. Return to Explore tab to view the new files.")
            else:
                st.error("Index regeneration failed. See details below.")

    elif mode == "clear":
        st.warning(
            "This action deletes generated sample content from docs, tickets, configs, and chat_history."
        )
        if st.button("Confirm Clear Sample Data", type="primary"):
            removed = clear_sample_data(remove_indexes=True)
            st.success(f"Removed {removed} item(s) and cleared indexes.")

    else:
        bucket = st.selectbox("View folder", DATA_BUCKETS, key="explore_bucket")
        if bucket == "chat_history":
            history = get_chat_history_messages()
            if not history:
                st.write("No stored chat history yet. Send a message in the chat tab to populate it.")
            else:
                personas = sorted(history.keys())
                selected_user = st.selectbox(
                    "Select persona",
                    personas,
                    key="history_persona",
                )
                messages = history.get(selected_user, [])
                if not messages:
                    st.write("No stored prompts for this persona yet.")
                else:
                    st.write(f"{len(messages)} stored user prompt(s) for `{selected_user}` (newest first).")
                    table_rows = [
                        {
                            "Timestamp": entry.get("timestamp") or "—",
                            "Message": entry.get("message", ""),
                        }
                        for entry in messages
                    ]
                    st.dataframe(table_rows, use_container_width=True)
        else:
            rows = list_bucket_contents(bucket)
            if not rows:
                st.write("No files found in this folder.")
            else:
                rows_display = [
                    {
                        "Name": row["name"],
                        "Size (KB)": row["size_kb"],
                    }
                    for row in rows
                ]
                st.table(rows_display)
                file_names = [row["name"] for row in rows]
                selected_file = st.selectbox("Preview file contents", file_names)
                if selected_file:
                    bucket_path = ensure_bucket(bucket)
                    file_path = bucket_path / selected_file
                    try:
                        suffix = file_path.suffix.lower()
                        if suffix == ".json":
                            with file_path.open("r", encoding="utf-8") as handle:
                                st.json(json.load(handle))
                        else:
                            text = file_path.read_text(encoding="utf-8", errors="ignore")
                            preview = text[:5000]
                            language = {
                                ".yaml": "yaml",
                                ".yml": "yaml",
                                ".py": "python",
                                ".md": "markdown",
                                ".html": "html",
                                ".csv": "csv",
                            }.get(suffix, "text")
                            st.code(preview, language=language)
                            if len(text) > len(preview):
                                st.caption("Preview truncated at 5000 characters.")
                    except Exception as exc:
                        st.error(f"Unable to display file contents: {exc}")


def main() -> None:
    render_sidebar()
    chat_tab, generate_tab, upload_tab = st.tabs([
        "Chat",
        "Generate Data",
        "Upload & Explore",
    ])

    with chat_tab:
        handle_chat_tab()
    with generate_tab:
        handle_generate_tab()
    with upload_tab:
        handle_upload_tab()


if __name__ == "__main__":
    main()
