# Vectorstore.py

import os
import uuid

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, Filter, FieldCondition, MatchValue, PayloadSchemaType
from typing import List, Dict

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_PORT = os.getenv("QDRANT_PORT", "6333") # Get port from environment, if not found, default to 6333
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "client_knowledge_base"



if not QDRANT_URL:
    raise ValueError("Missing QDRANT_URL in evironment")

if not QDRANT_API_KEY:
    raise ValueError("Missing QDRANT_API_KEY in environment")

# Initialize Qdrant client
client = QdrantClient(

    url = QDRANT_URL,
    api_key = QDRANT_API_KEY

)


def init_collection():
    # try:
    #     client.delete_collection(collection_name=COLLECTION_NAME)
    # except Exception as e:
    #     print(f"Collection deletion skipped: {e}")

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )

    # ✅ Create index on client_id
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="client_id",
        field_schema=PayloadSchemaType.KEYWORD
    )

    # Optional: index type too
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="type",
        field_schema=PayloadSchemaType.KEYWORD
    )

init_collection()

def upsert_vectors(texts: List[str], embeddings: List[List[float]], metadatas: List[Dict]):
    
    """
    Uploads vectors to the Qdrant collection after embedding the texts.
    Args:
        texts (List[str]): List of texts to be embedded and uploaded.
        embeddings (List[List[float]]): List of pre-computed embeddings for the texts.
        metadatas (List[Dict]): List of metadata dictionaries for each text.
    """
    points = [

        PointStruct(

            id=str(uuid.uuid4()),
            vector=embedding,
            payload=metadata | {"text": text}

        )

        for text, embedding, metadata in zip(texts, embeddings, metadatas)
    
    ]

    client.upsert(

        collection_name=COLLECTION_NAME,
        points=points

    )


def search_similar(query_embedding: List[float], client_id: str, top_k: int = 5) -> List[Dict]:

    """
    Searches for similar vectors in the Qdrant Collection based on the query(user_input) embedding.

    Args:
        query_embedding (List[float]): The embedding of the query text.
        client_id (str): The ID of the client(whose making request) to filter results.
        top_k (int): The number of top similar vectors to return after the search.
    
    Returns:
        List[Dict]: A List of dictionaries containing the text and metadata of the top similar vectors.
    """
    search_result = client.search(

        collection_name = COLLECTION_NAME,
        query_vector = query_embedding,
        limit = top_k,
        query_filter = Filter(

            must = [

                FieldCondition(

                    key="client_id",
                    match=MatchValue(
                        value=client_id
                        )
                )
            ]
        )
    )

    return [hit.payload['text'] for hit in search_result]


# print(QDRANT_URL, QDRANT_PORT, QDRANT_API_KEY, COLLECTION_NAME)

# def get_collection_name(): # This line ends with a colon
#     """ # This line MUST be indented
#     Returns the name of all the collections present in the Qdrant database.
#     """

#     return [c.name for c in client.get_collections().collections]

# a = get_collection_name()
# print(a)

