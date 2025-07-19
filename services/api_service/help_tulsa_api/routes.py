from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Dict, Deque
from collections import deque
import yaml
import os
import logging
from pathlib import Path
import json

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from help_tulsa_vectorizer.embedding import load_model

from .models import AskRequest, AskResponse, Resource
from .prompt import PREFIX, CLARIFY_PROMPT

router = APIRouter()
security = HTTPBearer()

logger = logging.getLogger("help_tulsa_api")
logging.basicConfig(level=logging.INFO, format='%(message)s')

RATE_LIMIT = 100
WINDOW = timedelta(minutes=10)
requests_log: Dict[str, Deque[datetime]] = {}

DATA_PATH = os.path.join("/app/data", "resources.yaml")
COLLECTION = "help_resources"
MODEL = None

def token_bucket(session: str):
    now = datetime.utcnow()
    bucket = requests_log.setdefault(session, deque())
    while bucket and (now - bucket[0]) > WINDOW:
        bucket.popleft()
    if len(bucket) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    bucket.append(now)


def get_qdrant_client():
    host = os.getenv("QDRANT_HOST", "localhost")
    port = int(os.getenv("QDRANT_PORT", 6333))
    return QdrantClient(host=host, port=port)


def search(question: str):
    global MODEL
    if MODEL is None:
        MODEL = load_model()
    client = get_qdrant_client()
    vector = MODEL.encode([question])[0]
    return client.search(
        collection_name=COLLECTION,
        query_vector=vector,
        limit=2,
        with_payload=True,
    )


def get_records():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH) as f:
        return yaml.safe_load(f) or []


@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    token_bucket(req.session_id)
    logger.info(
        json_log(session_id=req.session_id, question=req.question)
    )
    results = search(req.question)
    if not results:
        return AskResponse(answer=CLARIFY_PROMPT, resources=[])
    top_score = results[0].score
    records = [r.payload for r in results]
    resources = [Resource(**r) for r in records]
    if top_score < 0.5:
        answer = CLARIFY_PROMPT
    else:
        answer = PREFIX + resources[0].description
    return AskResponse(answer=answer, resources=resources)


def json_log(**data):
    data["timestamp"] = datetime.utcnow().isoformat()
    return json.dumps(data)


def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != os.getenv("ADMIN_TOKEN"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/admin/refresh", dependencies=[Depends(verify_admin)])
def admin_refresh():
    # simple signal via file touch
    Path(DATA_PATH).touch()
    return {"status": "refresh triggered"}
