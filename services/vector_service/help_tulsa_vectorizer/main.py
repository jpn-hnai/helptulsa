import json
import os
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "help_resources"


def main() -> None:
    data_file = Path("/app/data/resources.jsonl")
    if not data_file.exists():
        print(f"Data file {data_file} not found")
        return

    client = QdrantClient(host=os.getenv("QDRANT_HOST", "qdrant"), port=int(os.getenv("QDRANT_PORT", "6333")))
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client.recreate_collection(
        COLLECTION_NAME,
        vectors_config=rest.VectorParams(size=384, distance=rest.Distance.COSINE)
    )

    points = []
    with data_file.open() as f:
        for line in f:
            rec = json.loads(line)
            text = " ".join(str(v) for k, v in rec.items() if k != "id")
            vector = model.encode(text).tolist()
            points.append(rest.PointStruct(id=rec["id"], vector=vector, payload=rec))

    client.upsert(collection_name=COLLECTION_NAME, wait=True, points=points)
    print(f"Upserted {len(points)} records to {COLLECTION_NAME}")


if __name__ == "__main__":
    main()
