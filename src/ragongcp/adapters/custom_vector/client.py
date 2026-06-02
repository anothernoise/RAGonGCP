"""Custom Vector Search backend — STUB.

Planned: a fully self-managed pipeline for maximum control/cost-tuning:
  - chunk + embed documents with a Vertex `text-embedding-*` model,
  - upsert vectors into a Vertex AI Vector Search index,
  - query the index, hydrate chunk text from a metadata store (e.g. GCS/BigQuery).

Implement `ensure_corpus` (create/get index + endpoint), `upsert` (embed +
upsert datapoints), and `retrieve` (embed query -> find_neighbors -> Chunks).

Reference:
  https://cloud.google.com/vertex-ai/docs/vector-search/overview
"""

from __future__ import annotations

from ragongcp.config import ProfileConfig, Settings
from ragongcp.domain.models import Chunk, Document, Query

_NOT_IMPLEMENTED = (
    "custom_vector backend is a stub in this POC. "
    "Use backend=vertex_rag_engine (default) or backend=fake."
)


class CustomVectorBackend:
    def __init__(self, profile: ProfileConfig, settings: Settings) -> None:
        self.profile = profile
        self.settings = settings

    def ensure_corpus(self) -> str:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def upsert(self, documents: list[Document]) -> int:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def retrieve(self, query: Query) -> list[Chunk]:
        raise NotImplementedError(_NOT_IMPLEMENTED)
