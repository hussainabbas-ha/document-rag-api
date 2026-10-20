# Document RAG API

Retrieval-augmented generation API for uploaded documents. Files are chunked, embedded, stored in Qdrant, and queried through a FastAPI router.

## Getting started

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Configuration

| Variable | Purpose |
| --- | --- |
| `GEMINI_API_KEY` | Embeddings / generation |
| `QDRANT_URL` | Vector database URL |
| `QDRANT_API_KEY` | Vector database key |

## Routes

Routers are mounted under `/api` for upload and query.
