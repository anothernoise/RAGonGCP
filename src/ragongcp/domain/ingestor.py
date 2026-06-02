"""Ingestor port — the swappable ingestion interface.

An Ingestor takes already-staged documents (typically in GCS) and loads them
into the backend's corpus/index.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ragongcp.domain.models import Document


@runtime_checkable
class Ingestor(Protocol):
    """Loads documents into the active backend's corpus."""

    def ensure_corpus(self) -> str:
        """Create the corpus if it does not exist; return its identifier."""
        ...

    def upsert(self, documents: list[Document]) -> int:
        """Import/refresh the given documents. Return the count imported."""
        ...
