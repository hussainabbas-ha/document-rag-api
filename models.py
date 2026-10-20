# models.py

from pydantic import BaseModel
from typing import Literal, Optional, List


class UploadRequest(BaseModel):
    type: Literal["pdf", "qa"]
    client_id: str
    file_path: Optional[str] = None  # for PDF path (if sent by Laravel)
    qa_pairs: Optional[List[dict]] = None  # [{question: "...", answer: "..."}]


class QueryRequest(BaseModel):
    message: str
    client_id: str


class QueryResponse(BaseModel):
    response: str
    source: Optional[str] = None
