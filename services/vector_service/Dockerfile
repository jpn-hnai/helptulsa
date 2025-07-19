FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install --no-root
COPY help_tulsa_vectorizer ./help_tulsa_vectorizer
CMD ["python", "-m", "help_tulsa_vectorizer.main"]
