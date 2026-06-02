FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# Install dependencies first for better layer caching.
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

COPY config ./config

EXPOSE 8080
CMD ["sh", "-c", "uvicorn ragongcp.api.main:app --host 0.0.0.0 --port ${PORT}"]
