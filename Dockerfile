FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# Install uv package manager.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install dependencies first for better layer caching.
COPY pyproject.toml README.md ./
COPY src ./src
RUN uv sync --no-dev

COPY config ./config

EXPOSE 8080
CMD ["sh", "-c", "uv run uvicorn ragongcp.api.main:app --host 0.0.0.0 --port ${PORT}"]
