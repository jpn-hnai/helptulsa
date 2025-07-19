FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install --no-root
COPY help_tulsa_crawler ./help_tulsa_crawler
CMD ["python", "-m", "help_tulsa_crawler.main"]
