# Fine-Tuning Expert Chatbot (PDF RAG)

An end-to-end Retrieval-Augmented Generation (RAG) assistant that answers questions about your own PDF documents. The project combines PDF parsing (Docling), chunking, Milvus vector search, a Groq-hosted LLM, FastAPI for the backend, and a Streamlit chat UI. Conversation memory and prompt guardrails keep replies concise, grounded, and focused on LLM fine-tuning topics.

## Table of Contents
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Project Layout](#project-layout)
- [Quickstart](#quickstart)
  - [Install dependencies](#install-dependencies)
  - [Prepare data](#prepare-data)
  - [Ingest PDFs into Milvus](#ingest-pdfs-into-milvus)
  - [Run the FastAPI service](#run-the-fastapi-service)
  - [Run the Streamlit UI](#run-the-streamlit-ui)
- [Docker Images](#docker-images)
- [How It Works](#how-it-works)
  - [Ingestion pipeline](#ingestion-pipeline)
  - [Query pipeline](#query-pipeline)
- [Provided Screenshots](#provided-screenshots)
- [Troubleshooting](#troubleshooting)

## Features
- **PDF-aware answers**: Parses and chunks PDFs, storing dense embeddings in Milvus for semantic retrieval.
- **Guardrailed assistant**: System prompt enforces scope (LLM fine-tuning + supplied documents) and refusal rules for unrelated questions.
- **Conversation memory**: Summarizes prior turns and keeps recent context so follow-up questions remain coherent.
- **FastAPI backend**: Simple `/query` endpoint that returns grounded answers.
- **Streamlit chat UI**: Minimal, wide-layout chat surface that can call the FastAPI endpoint.
- **Docker-ready**: Separate Dockerfiles for API and UI for easy containerization.

## Architecture Overview
```
PDFs → Docling loader → Text chunks (LangChain splitters) → Milvus vector store
                                                ↓
                                        Groq LLM (OpenAI-compatible)
                                                ↓
                                    FastAPI RAG chain + guardrails
                                                ↓
                                   Streamlit conversational front-end
```

## Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) for dependency management (used by the Docker images and local commands)
- Access to a Milvus instance (URI + token)
- Groq API key (OpenAI-compatible endpoint)

## Configuration
Create a `.env` file in the project root with the required environment variables:

```bash
GROQ_API_KEY=your_groq_key
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=moonshotai/kimi-k2-instruct-0905

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

MILVUS_URI=http://localhost:19530
MILVUS_TOKEN=your_milvus_token
MILVUS_COLLECTION=pdf_rag_chunks

PDF_DIR=./data/pdfs
TOP_K=4
```

Adjust values for your deployment (e.g., Milvus cloud URI/token or a different Groq-compatible model).

## Project Layout
- `app/api` – FastAPI app, health + `/query` routes.
- `app/core` – Settings, embeddings, LLM factory, prompt guardrails, configuration.
- `app/ingestion` – PDF discovery, parsing (Docling), chunking, and Milvus indexing.
- `app/rag` – Retriever, conversation memory, and the RAG chain composition.
- `app/ui` – Streamlit chat UI.
- `scripts/ingest.py` – CLI to parse PDFs and populate Milvus.
- `docker/` – Dockerfiles for API and Streamlit services.

## Quickstart
### Install dependencies
```bash
uv sync
```

### Prepare data
Place your PDFs in `data/pdfs/` (create the folder if it does not exist). The ingestion script will crawl this directory.

### Ingest PDFs into Milvus
```bash
uv run python -m scripts.ingest
```
This will parse PDFs with Docling, split them into overlapping chunks, and push embeddings into your configured Milvus collection.

### Run the FastAPI service
```bash
uv run uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```
The API exposes `/health` and `/query`. Example query:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What fine-tuning steps are recommended?"}'
```

### Run the Streamlit UI
```bash
FASTAPI_URL=http://localhost:8000/query \
uv run streamlit run app/ui/streamlit_app.py --server.address=0.0.0.0 --server.port=8501
```
Open `http://localhost:8501` and chat with the assistant. The sidebar lists the stack and a button to clear chat history.

## Docker Images
Build and run the services independently:

```bash
# FastAPI
docker build -t pdf-rag-api -f docker/fastapi/Dockerfile .
docker run -p 8000:8000 --env-file .env pdf-rag-api

# Streamlit
docker build -t pdf-rag-ui -f docker/streamlit/Dockerfile .
docker run -p 8501:8501 --env FASTAPI_URL=http://host.docker.internal:8000 pdf-rag-ui
```

Both images rely on `uv` inside the container to install dependencies and start the relevant process.

## How It Works
### Ingestion pipeline
1. **Discover PDFs**: `scripts.ingest` finds files under `PDF_DIR` (defaults to `data/pdfs`).
2. **Parse**: `DoclingLoader` extracts structured text from each PDF (`app/ingestion/parse_docling.py`).
3. **Chunk**: `RecursiveCharacterTextSplitter` creates overlapping 500-character chunks (`app/ingestion/chunking.py`).
4. **Embed & index**: Chunks are embedded with the Hugging Face model and stored in Milvus (`app/ingestion/index_milvus.py`).

### Query pipeline
1. **Retrieve**: `/query` receives a question, uses Milvus retriever to fetch top-k chunks (`app/rag/retriever.py`).
2. **Guardrails**: A system prompt enforces scope and refusal rules (`app/core/prompts/guardrails.md`).
3. **LLM response**: Groq (OpenAI-compatible) generates an answer with context citation-style prefixes (`app/rag/chain.py`).
4. **Memory**: ConversationSummaryMemory summarizes older turns while keeping recent dialogue (`app/rag/memory.py`).

## Provided Screenshots
The user supplied four reference screenshots for context:
- **Chat UI walkthrough**: Demonstrates the Streamlit interface with a sidebar describing the stack and a clean chat layout. The instructions highlight answering questions with sources grounded in PDFs.
- **Vector store dashboard**: Shows Milvus collections populated with parsed documents and embeddings.
- **GitHub deploy view**: Displays repository deploy tags and release history, confirming container build artifacts.
- **Docker compose logs**: Terminal view illustrating the API startup, environment variables, and container health during deployment.

You can embed these images in your own documentation (e.g., `docs/images/ui.png`, `docs/images/milvus.png`, etc.) to mirror the same workflow snapshots.

## Troubleshooting
- **No PDFs found**: Ensure files exist in `data/pdfs/` before running `scripts.ingest`.
- **Milvus connection errors**: Verify `MILVUS_URI`/`MILVUS_TOKEN` and that the service is reachable from where you run ingestion/API.
- **Groq authentication**: Check `GROQ_API_KEY` and confirm your account has access to the specified model.
- **Slow responses**: Reduce chunk size/overlap, lower `TOP_K`, or ensure Milvus/LLM endpoints are close to your runtime environment.

