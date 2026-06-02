"""Vertex AI Search (Agent Builder) backend — STUB.

Planned: back retrieval with a Vertex AI Search data store + serving config
(fully managed search with Drive/site connectors). Implement `ensure_corpus`
(create/get data store + engine), `upsert` (import documents into the data
store), and `retrieve` (search serving config -> Chunks).

Reference:
  https://cloud.google.com/generative-ai-app-builder/docs/introduction
"""

from __future__ import annotations

from ragongcp.config import ProfileConfig, Settings
from ragongcp.domain.models import Chunk, Document, Query

_NOT_IMPLEMENTED = (
    "vertex_search backend is a stub in this POC. "
    "Use backend=vertex_rag_engine (default) or backend=fake."
)


class VertexSearchBackend:
    def __init__(self, profile: ProfileConfig, settings: Settings) -> None:
        self.profile = profile
        self.settings = settings

    def ensure_corpus(self) -> str:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def upsert(self, documents: list[Document]) -> int:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def retrieve(self, query: Query) -> list[Chunk]:
        raise NotImplementedError(_NOT_IMPLEMENTED)
