# HelpTulsa.ai Microservices

This repository contains a minimal, container-native setup for processing mental-health resources.

## Services

- **crawler_service**: converts `inputs/resources.xlsx` to `data/resources.jsonl`.
- **vector_service**: embeds records with Sentence-Transformers and stores them in Qdrant.
- **api_service**: exposes endpoints for semantic search and refreshing data.

## Usage

1. Copy `.env.example` to `.env` and adjust values if needed.
2. Place `resources.xlsx` in the `inputs/` directory.
3. Run `docker compose up --build`.

The API will be available at `http://localhost:8000`.
