from help_tulsa_api.routes import search, MODEL, COLLECTION
from help_tulsa_api.models import AskRequest
from help_tulsa_api.routes import ask
from help_tulsa_api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_ask_endpoint(qdrant, resources_file):
    # ensure vector index exists
    from help_tulsa_vectorizer.main import embed_and_upsert
    embed_and_upsert()
    req = {"session_id": "test", "question": "desc"}
    resp = client.post("/ask", json=req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["resources"]
    assert float(qdrant.count(collection_name=COLLECTION).count) >= 1
    assert data["resources"][0]["description"] == "desc"
