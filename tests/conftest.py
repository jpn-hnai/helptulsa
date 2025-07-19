import pytest
from qdrant_client import QdrantClient
import yaml
from pathlib import Path
import docker
import time
import sys
sys.path.extend([
    str(Path(__file__).resolve().parents[1] / 'services' / 'api_service'),
    str(Path(__file__).resolve().parents[1] / 'services' / 'vector_service'),
])

@pytest.fixture(scope="session")
def resources_file(tmp_path_factory):
    data = [
        {"id": "1", "name": "A", "description": "desc", "url": "http://a", "phone": "123"}
    ]
    path = tmp_path_factory.getbasetemp() / "resources.yaml"
    with open(path, "w") as f:
        yaml.safe_dump(data, f)
    dest = Path("/app/data/resources.yaml")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(path.read_text())
    return dest


@pytest.fixture(autouse=True)
def dummy_model(tmp_path_factory, monkeypatch):
    model_dir = Path(".models/all-MiniLM-L6-v2")
    model_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("MODEL_DIR", str(Path(".models")))
    yield model_dir

@pytest.fixture(scope="session")
def qdrant(tmp_path_factory):
    container = None
    try:
        client = docker.from_env()
        container = client.containers.run(
            "qdrant/qdrant:v1.9.2",
            ports={"6333/tcp": 6333},
            detach=True,
        )
    except Exception as e:
        pytest.skip(f"Docker unavailable: {e}")
    # wait for qdrant to be ready
    qc = QdrantClient(host="localhost", port=6333)
    for _ in range(30):
        try:
            qc.get_collections()
            break
        except Exception:
            time.sleep(1)
    yield qc
    if container:
        container.remove(force=True)
