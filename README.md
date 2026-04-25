# AI Research & Report Agent

A production-ready AI system that accepts research queries, retrieves relevant documents via FAISS, orchestrates a LangGraph workflow, and returns structured JSON analysis through a FastAPI backend.

## Features
- FastAPI backend with `/health` and `/analyze`
- Groq LLM integration via `llama-3.1-8b-instant`
- LangGraph multi-step agent orchestration
- FAISS vector retrieval with document chunking and Sentence Transformers embeddings
- Simple HTML/JS frontend demo
- Docker-ready and deployable on Render

## Project structure
- `app.py` — FastAPI entrypoint
- `backend/` — modular backend implementation
- `frontend/` — static demo UI
- `data/docs/` — document source files for RAG
- `data/vectorstore/` — FAISS index storage
- `Dockerfile` — container build
- `render.yaml` — Render deployment config

## Setup
1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Create `.env` from the template and set `GROQ_API_KEY`.
3. Add research documents under `data/docs/`.
4. Start the backend:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```
5. Open the demo UI at:
   ```
   http://localhost:8000/static/index.html
   ```

## API
- `GET /health` — service health check
- `POST /analyze` — analyze a query

Example payload:
```json
{
  "query": "Summarize the latest research on autonomous systems risk management."
}
```

## Render Deployment
1. Connect this repository to Render.
2. Use Docker with `Dockerfile`.
3. Set environment variable `GROQ_API_KEY` in Render secrets.
4. Deploy the service.

## Notes
- The project automatically builds a FAISS index when first requested.
- Add or refresh documents by updating `data/docs/` and deleting `data/vectorstore/faiss.index` and `metadata.json`.
