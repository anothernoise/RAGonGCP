"""Offline Generator — composes an answer from context without calling an LLM.

Used when backend=fake (and in tests) so the full pipeline + API run without GCP
credentials. It stitches together the top passages and cites them, mirroring the
shape of a real grounded answer.
"""

from __future__ import annotations

from ragongcp.domain.models import Answer, Chunk
from ragongcp.generation.prompt import extract_citations


class EchoGenerator:
    def generate(self, question: str, chunks: list[Chunk]) -> Answer:
        if not chunks:
            return Answer(text="I don't know — no relevant context was found.", model="echo")
        body = " ".join(
            f"{chunk.text.strip()} [{i}]" for i, chunk in enumerate(chunks[:3], start=1)
        )
        text = f"Based on the retrieved sources: {body}"
        return Answer(
            text=text,
            citations=extract_citations(text, chunks),
            chunks=chunks,
            model="echo",
        )
