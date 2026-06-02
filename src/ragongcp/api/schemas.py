"""Request/response schemas for the HTTP API."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ragongcp.domain.models import Citation, Document


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=50)


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    model: str | None = None


class IngestRequest(BaseModel):
    documents: list[Document]


class IngestResponse(BaseModel):
    imported: int
    corpus: str


class HealthResponse(BaseModel):
    status: str
    profile: str
    backend: str
