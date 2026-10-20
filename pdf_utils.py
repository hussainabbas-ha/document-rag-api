# pdf_utils.py

from PyPDF2 import PdfReader
from typing import List
import re


def extract_pdf_chunks(pdf_path: str, max_chunk_size: int = 1000) -> List[str]:
    """
    Reads a PDF file and returns a list of text chunks (max_chunk_size tokens each).
    """
    try:
        reader = PdfReader(pdf_path)
        full_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        raise RuntimeError(f"Failed to read PDF: {str(e)}")

    # Clean up spacing and line breaks
    full_text = re.sub(r"\s+", " ", full_text).strip()

    # Simple sentence-based chunking
    sentences = re.split(r'(\.|\!|\?)\s', full_text)
    chunks, current = [], ""

    for sentence in sentences:
        if len(current) + len(sentence) < max_chunk_size:
            current += sentence + " "
        else:
            chunks.append(current.strip())
            current = sentence + " "

    if current.strip():
        chunks.append(current.strip())

    return chunks
