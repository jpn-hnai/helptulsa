FROM python:3.11-slim
WORKDIR /app
COPY services/api_service/pyproject.toml ./pyproject.toml
COPY services/vector_service/help_tulsa_vectorizer ./help_tulsa_vectorizer
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY services/api_service/help_tulsa_api ./help_tulsa_api
CMD ["help-tulsa-api"]
