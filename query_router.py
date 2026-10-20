# routers/query_router.py

from fastapi import APIRouter, HTTPException
from models import QueryRequest, QueryResponse
from embed import embed_texts, generate_answer
from vectorstore import search_similar, upsert_vectors

router = APIRouter()

@router.post("/respond", response_model=QueryResponse)
def handle_user_query(request: QueryRequest):
    query = request.message
    client_id = request.client_id

    if not query or not client_id:
        raise HTTPException(status_code=400, detail="Missing message or client_id")

    try:
        embedding = embed_texts([query])[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")

    try:
        context_chunks = search_similar(query_embedding=embedding, client_id=client_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    if not context_chunks:
        return QueryResponse(response="Sorry, I couldn't find relevant info.")

    full_context = "\n\n".join(context_chunks)

    try:
        response = generate_answer(full_context, query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini response failed: {str(e)}")

    return QueryResponse(response=response, source="rag")
