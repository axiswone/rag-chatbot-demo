# RAG-Powered Chatbot Demo

A hands-on reference project showing how to ground LLM responses in organizational knowledge with the full Retrieval Augmented Generation or RAG lifecycle (data ingestion -> indexing -> retrieval orchestration -> UX). 
The repo bundles a FastAPI backend with LangChain, FAISS vector stores, synthetic data generators, and a Streamlit workbench so you can go from zero to a fully functioning contextual chatbot without wiring things together yourself. Whether you are new to RAG or already shipping production pipelines, this repo is designed to be a living playbook: beginners get a guided "push button" path, while experienced developers can dive straight into LangChain, FastAPI, and FAISS internals. 

---

## ⭐ Like What You See?
If this project helped you, inspired you, or saved you time, consider giving it a ⭐! It helps others discover it and keeps the momentum going.

---

## 💬 Share Your Thoughts
We use [GitHub Discussions](https://github.com/Uma-Ramanathan-1/rag-chatbot-demo/discussions) to gather feedback and ideas. Jump into our [Feedback & Ideas Thread](https://github.com/Uma-Ramanathan-1/rag-chatbot-demo/discussions/1) and let’s chat!

---

## What This Demo Showcases

- **Multi-source retrieval:** A LangChain `MultiRetrievalQAChain` fans out across docs, tickets, configs, and semantic chat history so every answer is grounded in multiple evidence types.
- **Persona-aware prompts:** Requests include role, activity, and preference hints, demonstrating how to tailor LLM tone without custom models.
- **Streamlit operations console:** Generate data, upload real files, rebuild indexes, trim history, and chat--all from a single dashboard that mirrors the CLI flows.
- **Synthetic + bring-your-own data ingestion:** Faker-powered generators let you practice without sensitive data, while the same pipeline happily indexes your actual Markdown/JSON/YAML assets.
- **Open-source / free LLM inferencing:** Swap `ChatOpenAI` for Groq, Ollama, or any LangChain-compatible provider to run the entire pipeline without paid APIs.
- **Transparent observability:** `logs/chat.log` captures each request/response pair plus backend traces so you can trace routing decisions and failures.

If you just want to try the experience, jump to [Quickstart](#quickstart). For architectural context, see `ARCHITECTURE.md`.

---

## Repository Layout

```
rag-chatbot-demo/
|-- backend/             # FastAPI app, FAISS indexes, scripts, venv/
|   |-- app/             # API, chains, chat history utils
|   |-- data/            # Generated docs/tickets/configs + vector stores
|   `-- scripts/         # Index builders (generate_*_index.py, generate_indexes.py)
|-- data-generators/     # Synthetic data pipeline + domain configs
|-- frontend/            # Streamlit dashboard + minimal HTML landing page
|-- logs/                # Runtime + chat transcripts (logs/chat.log)
`-- ARCHITECTURE.md      # System design notes
```

---

## Requirements

- Python 3.12 (recommended due to LangChain dependencies)
- `pip` and a virtual environment tool (`python -m venv` works)
- An OpenAI API key or credentials for a drop-in alternative (Groq, Ollama, etc.)

Optional:

- Git (if you plan to pull updates)
- Make / Bash for scripted workflows (not required on Windows)

---

## Quickstart

The steps below assume PowerShell (Windows) or any POSIX shell and that you are running commands from the repository root (`rag-chatbot-demo/`). Adjust paths if you prefer another shell. If you are new to RAG, treat the steps as a checklist you can follow verbatim; if you already have data and embeddings in place, skim for the pieces you care about (for example, jump straight to Step 6 after ensuring indexes exist).

### 1. Create and activate a virtual environment

```powershell
py -3.12 -m venv backend\venv
.\backend\venv\Scripts\activate
```

```bash
python -m venv backend/venv   # ensure your python points to 3.12
source backend/venv/bin/activate
```

### 2. Install backend + tooling dependencies

```bash
pip install -r backend/requirements.txt
```

You do not need Node/npm; Streamlit covers the UI.

### 3. Configure environment variables

```bash
cp backend/.env.example backend/.env   # or copy via File Explorer on Windows
```

Populate at least `OPENAI_API_KEY`. To use a free provider:

- Groq: install `langchain-groq`, set `GROQ_API_KEY`, and swap `ChatOpenAI` in `backend/app/main.py` for `ChatGroq`.
- Ollama: install `langchain-ollama`, run `ollama pull llama3:8b`, and swap the chat model accordingly.

### 4. Load knowledge sources

Pick whichever path matches your environment; every CLI action below also has a Streamlit equivalent so non-terminal users stay productive.

**Option A: Generate synthetic data (docs, tickets, configs, chat history)**

```bash
cd data-generators
python generate_sample_data.py         # respects config.yaml / .env overrides
cd ..
```

- Writes Faker-powered samples into `backend/data/`.
- Tweak `data-generators/config.yaml` (defaults to the `tech` domain) or export env vars such as `DATA_DOMAIN=finance`, `DATA_VOLUME=large`, etc.
- In the Streamlit "Generate Data" tab, the "Generate Data" button runs this command and rebuilds indexes afterward. You have the option to retain existing Data or remove it.

**Option B: Bring your own real data**

- Drop Markdown/text/JSON/YAML files into `backend/data/docs`, `tickets`, `configs`, or `chat_history`.
- Make sure files use UTF-8 and include enough metadata (severity, timestamps, etc.) if you want that surfaced in answers.
- In the Streamlit "Upload and Explore" tab, the "Upload Files" button allows you upload your data (same storage location under the hood), and automatically rebuilds the indexes.

### 5. Build FAISS indexes

> **Using Streamlit?** The Data Generation and Upload tabs already rebuild FAISS indexes after each run/upload. Use the CLI below only when you need manual control from the terminal.

```bash
cd backend/scripts
python generate_indexes.py     # runs all individual generators
cd ../..
```

Indexes for docs, tickets, configs, and chat history are saved under `backend/data/*_index`. If a store is missing, the FastAPI app will raise a descriptive error telling you to regenerate.

### 6. Run the FastAPI backend

From the repo root

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

- API docs: http://localhost:8000/docs
- Sample request:

```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"user_query\":\"How do I redeploy staging?\",\"user_id\":\"demo\"}"
```

### 7. Launch the Streamlit dashboard

You need to be in a terminal with the virtualenv activated (See Step 1). 
From the repo root,

```bash
cd frontend
streamlit run streamlit_app.py
```

Set `BACKEND_URL` as an environment variable before launching Streamlit if your FastAPI server runs on a different host/port (for example, `BACKEND_URL=http://localhost:9000 streamlit run streamlit_app.py` on macOS/Linux or `$env:BACKEND_URL=\"http://localhost:9000\"; streamlit run streamlit_app.py` in PowerShell).

---

## Configurable Environment Variables

**Backend (`backend/.env`):**

- `OPENAI_API_KEY` - primary credential for ChatOpenAI; swap for another provider's key when you change the `llm` wiring.
- `EMBEDDING_MODEL` - HuggingFace embedding model name. Must match whatever model was used to build the FAISS stores; change it only if you plan to regenerate every index with the new embeddings.
- `LLM_MODEL` - default model variant passed to `ChatOpenAI`. Adjust when toggling GPT-4o/4.1-mini/etc.
- `TOP_K_RETRIEVAL` - number of chunks each retriever returns. Increasing improves recall but costs latency.
- `CHAT_HISTORY_LIMIT` - how many turns to retrieve from semantic memory per request. Higher values surface longer conversations but slow embedding lookups.
- `DEFAULT_USER_ROLE`, `DEFAULT_USER_PREFERENCES`, `DEFAULT_USER_ACTIVITY` - persona strings injected when the client does not provide them; useful for testing different prompt personas without changing the frontend.
- `BACKEND_URL` (set in your shell before running Streamlit) - tells the dashboard which FastAPI host/port to call.

**Data generator (`data-generators/.env`):**

- `DATA_DOMAIN`, `DATA_VOLUME`, `DATA_COMPLEXITY` - control which sector template is used and how much content is produced in each run.
- `OUTPUT_DIR`, `OVERWRITE_EXISTING` - change where generated docs/tickets/configs land and whether existing files get replaced.
- `DATA_LANGUAGE`, `INCLUDE_EXAMPLES`, `INCLUDE_TROUBLESHOOTING` - toggle language and enrichment extras in the synthesized manuals/tickets.
- Domain-specific lists such as `TECH_FOCUS_AREAS`, `HEALTHCARE_SPECIALTIES`, `FINANCE_REGULATIONS`, etc., let you bias the generated corpus toward the jargon you need.
- `SEED` - set to an integer to make generation deterministic for demos/tests.

---

## Synthetic Data Generation

`data-generators/generate_sample_data.py` creates realistic placeholder data with Faker when you do not have real documents yet:

- **Domain presets:** choose `tech`, `healthcare`, `finance`, `ecommerce`, or `general` in `config.yaml`, `.env`, or via env vars such as `DATA_DOMAIN`. Each preset exposes settings like `TECH_FOCUS_AREAS` or `FINANCE_REGULATIONS` so the generated text uses the right subject matter.
- **Volume and complexity controls:** `DATA_VOLUME` and `DATA_COMPLEXITY` determine how many items are generated and how detailed they are.
- **Output buckets:** the script writes Markdown/JSON/YAML into `backend/data/docs`, `tickets`, `configs`, and `chat_history`, adding severity, priority, persona, and timestamp metadata to resemble real incidents.
- **Bring your own data:** drop existing Markdown/text/JSON/YAML files into the same `backend/data/*` folders (or upload through the Streamlit UI) and rerun the index scripts to include them.
- **Automatic indexing:** FAISS scripts embed whatever is under `backend/data`, so changing domains or volume instantly changes what the chatbot can retrieve--no backend edits required.

---

## Streamlit Workbench Highlights

- Chat tab: talk to the model, inspect retrieved citations, manage semantic history by user ID, and download transcripts.
- Data generation tab: tweak knobs (domain, volume, complexity) and run `generate_sample_data.py` plus index rebuilds without touching the CLI.
- Uploads tab: drag-and-drop Markdown/text/JSON/YAML files directly into the right data bucket; Streamlit will re-index after ingestion.
- Data explorer tab: browse raw files per bucket, delete stale assets, and see index statistics.
- Maintenance shortcuts: clear all synthesized data, reset the current chat session, and check backend health via a live badge.

The UI calls the same scripts under the hood, so command-line and Streamlit workflows stay interchangeable.

---

## Suggested Queries to Kick Off Testing

If you are using synthetic data, you may examine the created documents to come up with queries that are relevant to the generated documents. e.g.

- **Probe an incident (tech defaults):** start with "Our staging deployment failed -- what logs should I check?" -> follow up "Generate a remediation checklist for recurrent deployment timeouts."
- **Switch domains via synthetic data:** after generating healthcare data, open with "We are a healthcare provider; how do HIPAA and telemedicine policies interact here?" -> then ask "What escalation steps does support take for oncology tickets marked high severity?" -> finish with "Summarize the compliance controls configured in our system YAML."
- **Leverage chat history:** start with "Summarize what `<user_id>` has been reporting about <topic> this month." -> continue with "What actions have we already suggested to `<user_id>` for those issues?" -> wrap with "Draft an update back to `<user_id>` referencing the past advice and any new guidance."

These prompts exercise each retriever and make it obvious when an index is missing or stale.

---

## Data and Index Lifecycle

1. Generate content via `data-generators/generate_sample_data.py` **or** drop your own Markdown/JSON/YAML artifacts into `backend/data/`. Domains (tech, healthcare, finance, ecommerce, general) plug in specialized writers (see `data-generators/domains/`). Every run--or file upload--creates docs, configs, tickets, and chat logs under `backend/data/`.
2. Embed into FAISS using `backend/scripts/generate_docs_index.py`, `generate_tickets_index.py`, etc., or the umbrella `generate_indexes.py`. If you need custom paths, update `app.config` (index locations) and the loader scripts before running them.
3. Serve through FastAPI: `app/main.py` loads the FAISS stores with a shared HuggingFace embedding model (`sentence-transformers/all-MiniLM-L6-v2` by default) and wires them into a `MultiRetrievalQAChain`.
4. Persist history: every chat turn is embedded and appended to `backend/data/chat_history_index`, enabling semantic recall beyond the fixed data buckets.

Need to reset? Use the Streamlit "Clear Sample data" button (Upload & Explore tab) or delete the contents of `backend/data/` and rerun `python backend/scripts/generate_indexes.py`.

---

## Logging and Monitoring

- `logs/chat.log` records every interaction (user query, routed chain, errors). Tail it while iterating:

  ```bash
  Get-Content logs/chat.log -Wait   # PowerShell
  tail -f logs/chat.log             # macOS/Linux
  ```
- Each log block contains the full request/response pair plus every backend trace step, so you can correlate what the user asked with the exact retrieval/chain flow that ran.

- FastAPI stdout surfaces retriever load problems and LangChain warnings.
- Streamlit prints subprocess output for data/index commands directly in the UI.

---

## Troubleshooting

- `RuntimeError: Failed to load docs index`: ensure you created sample data and ran the index scripts. The error message tells you which path is missing.
- `Missing some input keys` in chat logs: requests must include `user_query` and optional persona fields (`user_role`, `user_preferences`, `user_activity`). The Streamlit client already sends them; hand-written API calls must do the same.
- Slow first response: HuggingFace embeddings download the first time you start the backend. Keep the `venv` around to avoid repeated downloads.
- Switching LLM providers: install the corresponding LangChain integration, set provider-specific env vars, and update the `llm = ...` section in `backend/app/main.py`. Everything else remains unchanged.
- Clearing corrupted indexes: delete the relevant `backend/data/*_index` folder and rerun `generate_indexes.py`.

---

## Contributing and Next Steps

- Extend `data-generators/domains/` with your own sector-specific corpus.
- Add a persistent database (PostgreSQL) for audit-grade chat history; hooks already exist in `app/chat_history.py`.
- Harden auth/CORS in `app/main.py` before exposing this beyond localhost.
- Wire in evaluation notebooks (RAGAS, LlamaIndex evals) if you want scoring.

Feel free to copy sections of this README into internal docs or presentations. If you run into gaps, drop an issue or ping in chat and we can fill them in.

---

Happy building!
