import os
import subprocess
from typing import List

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "help_resources"

app = FastAPI()
client = QdrantClient(host=os.getenv("QDRANT_HOST", "qdrant"), port=int(os.getenv("QDRANT_PORT", "6333")))
model = SentenceTransformer("all-MiniLM-L6-v2")
admin_token = os.getenv("ADMIN_TOKEN", "changeme")


class AskRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/ask")
def ask(req: AskRequest):
    vector = model.encode(req.query).tolist()
    hits = client.search(collection_name=COLLECTION_NAME, query_vector=vector, limit=req.top_k)
    return {"results": [h.payload for h in hits]}


@app.post("/admin/refresh")
def refresh(x_token: str = Header(..., alias="X-Token")):
    if x_token != admin_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    print("Running crawler and vector services")
    subprocess.run(["docker", "compose", "run", "--rm", "crawler"], check=False)
    subprocess.run(["docker", "compose", "run", "--rm", "vector"], check=False)
    return {"status": "jobs launched"}

