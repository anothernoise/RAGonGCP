"""Retriever port — the swappable retrieval interface.

Each backend (Vertex RAG Engine, Vertex Search, custom vector store, fake)
implements this Protocol. Nothing above the adapters layer depends on a concrete
backend; the factory wires the right one from config.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ragongcp.domain.models import Chunk, Query


@runtime_checkable
class Retriever(Protocol):
    """Retrieves relevant context chunks for a query."""

    def ensure_corpus(self) -> str:
        """Create the corpus if it does not exist; return its identifier."""
        ...

    def retrieve(self, query: Query) -> list[Chunk]:
        """Return the top context chunks for the query, most relevant first."""
        ...
