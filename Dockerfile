FROM python:3.12-slim

WORKDIR /app

COPY backend/pyproject.toml ./
COPY backend/src ./src

RUN pip install --no-cache-dir .

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "uvicorn careergraph.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
