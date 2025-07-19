from typing import List, Dict
from uuid import uuid4
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
import os


def get_qdrant_client() -> QdrantClient:
    host = os.getenv("QDRANT_HOST", "localhost")
    port = int(os.getenv("QDRANT_PORT", 6333))
    return QdrantClient(host=host, port=port)


def ensure_collection(client: QdrantClient, name: str, dim: int = 384):
    if name not in [c.name for c in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=name,
            vectors_config=qmodels.VectorParams(size=dim, distance="Cosine"),
        )


def upsert_vectors(client: QdrantClient, collection: str, records: List[Dict], vectors: List[List[float]]):
    ensure_collection(client, collection)
    points = [
        qmodels.PointStruct(id=str(r.get("id") or uuid4()), vector=v, payload=r)
        for r, v in zip(records, vectors)
    ]
    client.upsert(collection_name=collection, points=points)
