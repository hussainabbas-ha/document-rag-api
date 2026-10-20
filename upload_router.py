# routers/upload_router.py

from fastapi import APIRouter, HTTPException
from models import UploadRequest
from embed import embed_texts
from pdf_utils import extract_pdf_chunks
from vectorstore import upsert_vectors
from uuid import uuid4

router = APIRouter()

@router.post("/upload")
def handle_upload(payload: UploadRequest):
    client_id = payload.client_id
    doc_id = str(uuid4())

    if payload.type == "pdf":
        if not payload.file_path:
            raise HTTPException(status_code=400, detail="file_path is required for type=pdf")

        try:
            chunks = extract_pdf_chunks(payload.file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

        try:
            embeddings = embed_texts(chunks)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")

        metadatas = [{"client_id": client_id, "type": "pdf", "chunk_index": i} for i in range(len(chunks))]
        upsert_vectors(texts=chunks, embeddings=embeddings, metadatas=metadatas)

        return {"status": "success", "source": "pdf", "chunks": len(chunks)}

    elif payload.type == "qa":
        if not payload.qa_pairs:
            raise HTTPException(status_code=400, detail="qa_pairs is required for type=qa")

        qa_chunks = [f"Q: {qa['question']}\nA: {qa['answer']}" for qa in payload.qa_pairs]

        try:
            embeddings = embed_texts(qa_chunks)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")

        metadatas = [
            {"client_id": client_id, "type": "qa", "qa_index": i} for i in range(len(qa_chunks))
        ]
        upsert_vectors(texts=qa_chunks, embeddings=embeddings, metadatas=metadatas)

        return {"status": "success", "source": "qa", "qa_count": len(qa_chunks)}

    else:
        raise HTTPException(status_code=400, detail="Invalid upload type")
