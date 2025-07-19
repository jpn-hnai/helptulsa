FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install --no-root
COPY help_tulsa_api ./help_tulsa_api
CMD ["uvicorn", "help_tulsa_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
