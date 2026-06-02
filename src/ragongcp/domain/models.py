"""Core domain models shared across adapters, generation, and the API.

These are backend-agnostic: a Vertex RAG Engine retriever, a custom vector
retriever, or a fake all speak in terms of these types.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Document(BaseModel):
    """A source document to be ingested into a corpus."""

    uri: str = Field(..., description="Canonical source location, e.g. gs://… or https://…")
    title: str | None = None
    mime_type: str = "text/plain"
    metadata: dict[str, str] = Field(default_factory=dict)


class Chunk(BaseModel):
    """A retrieved passage of context with provenance and a relevance score."""

    text: str
    source_uri: str
    title: str | None = None
    score: float = 0.0
    metadata: dict[str, str] = Field(default_factory=dict)


class Query(BaseModel):
    """A user query plus optional retrieval overrides."""

    text: str
    top_k: int | None = None
    filters: dict[str, str] = Field(default_factory=dict)


class Citation(BaseModel):
    """A first-class citation surfaced alongside a generated answer.

    `index` is the [n] marker used inline in the answer text.
    """

    index: int
    source_uri: str
    title: str | None = None
    snippet: str | None = None


class Answer(BaseModel):
    """The final grounded answer returned to the caller."""

    text: str
    citations: list[Citation] = Field(default_factory=list)
    chunks: list[Chunk] = Field(default_factory=list)
    model: str | None = None
    usage: dict[str, int | float | str] = Field(default_factory=dict)
