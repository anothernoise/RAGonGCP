"""Generator port — grounded answer generation.

Implementations take a question plus retrieved chunks and produce an Answer with
inline citations. The default implementation uses Gemini.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ragongcp.domain.models import Answer, Chunk


@runtime_checkable
class Generator(Protocol):
    """Generates a grounded, cited answer from a question and context chunks."""

    def generate(self, question: str, chunks: list[Chunk]) -> Answer:
        """Produce a grounded Answer. Must not invent sources outside `chunks`."""
        ...
