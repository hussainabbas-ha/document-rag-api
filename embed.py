# embed.py

import google.generativeai as genai
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# embedding_model = genai.embedder.EmbedContent(model="models/embedding-001")
chat_model = genai.GenerativeModel("gemini-1.5-pro")


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Embed a list of texts using Gemini embedding-001 model.
    Note: Embedding API is limited. Simulate if not available in SDK.
    """
    embeddings = []
    for text in texts:
        try:
            response = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            embeddings.append(response["embedding"])
        except Exception as e:
            raise RuntimeError(f"Embedding failed: {str(e)}")
    return embeddings

def generate_answer(context: str, query: str) -> str:
    """
    Takes the context and the user query, then uses Gemini to generate an answer.
    """
    prompt = f"""
You are a helpful assistant for a social media management company.
Answer the customer's question using the provided context. If the answer is not in the context, politely say you don’t know.

Context:
{context}

Question:
{query}

Answer:
    """

    response = chat_model.generate_content(prompt)
    return response.text.strip() if response else "Sorry, I don't know the answer right now."
