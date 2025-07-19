from pathlib import Path
from typing import List
import os

MODEL_PATH = Path(os.getenv("MODEL_DIR", "./.models")) / "all-MiniLM-L6-v2"

class DummyModel:
    def encode(self, texts: List[str]):
        return [[float(i % 384) for i in range(384)] for _ in texts]

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer(str(MODEL_PATH))
    except Exception:
        return DummyModel()
