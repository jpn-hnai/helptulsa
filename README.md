# HelpTulsa.ai

Container-native microservices for managing Tulsa mental health resources. The system ingests data, generates vector embeddings, and serves a FastAPI endpoint for questions.

## Quickstart

```bash
cp .env.example .env
docker compose up --build
# In another terminal
docker compose run --rm api_service pytest
```

Use the `/admin/refresh` endpoint with the `ADMIN_TOKEN` to re-ingest resources.

### Local Model Setup

Embeddings require the `all-MiniLM-L6-v2` model stored under `./.models`. Run the following once to cache it:

```python
from sentence_transformers import SentenceTransformer
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2').save('./.models/all-MiniLM-L6-v2')
```
