FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY help_tulsa_vectorizer ./help_tulsa_vectorizer
CMD ["help-tulsa-vectorizer"]
