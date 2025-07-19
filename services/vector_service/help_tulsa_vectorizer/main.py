from pathlib import Path
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .embedding import load_model
import time
from .qdrant_client import get_qdrant_client, upsert_vectors

DATA_PATH = Path("/app/data/resources.yaml")
COLLECTION = "help_resources"
model = None


def load_records():
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH) as f:
        return yaml.safe_load(f) or []


def embed_and_upsert():
    global model
    if model is None:
        model = load_model()
    records = load_records()
    if not records:
        return 0
    texts = [r.get("description", "") for r in records]
    vectors = model.encode(texts)
    client = get_qdrant_client()
    upsert_vectors(client, COLLECTION, records, vectors)
    return len(records)


def watch_file():
    class ReloadHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path == str(DATA_PATH):
                embed_and_upsert()

    observer = Observer()
    observer.schedule(ReloadHandler(), path=str(DATA_PATH.parent))
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


def main():
    embed_and_upsert()
    watch_file()

if __name__ == "__main__":
    main()
