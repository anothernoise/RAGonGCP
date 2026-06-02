"""Prompt assembly + citation extraction — pure functions, no SDK needed.

Kept separate from the Gemini client so it can be unit-tested offline and reused
by any generator implementation.
"""

from __future__ import annotations

import re

from ragongcp.domain.models import Chunk, Citation

_CITE_RE = re.compile(r"\[(\d+)\]")


def format_context(chunks: list[Chunk]) -> str:
    """Render numbered context passages the model can cite as [n]."""
    lines = []
    for i, chunk in enumerate(chunks, start=1):
        source = chunk.title or chunk.source_uri
        lines.append(f"[{i}] (source: {source})\n{chunk.text}")
    return "\n\n".join(lines)


def build_prompt(system_prompt: str, question: str, chunks: list[Chunk]) -> str:
    """Assemble the full grounded-generation prompt."""
    context = format_context(chunks) or "(no context retrieved)"
    return (
        f"{system_prompt.strip()}\n\n"
        f"Context passages:\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer (cite sources inline as [n]):"
    )


def extract_citations(answer_text: str, chunks: list[Chunk]) -> list[Citation]:
    """Map the [n] markers actually used in the answer back to source chunks."""
    used_indices = sorted({int(m) for m in _CITE_RE.findall(answer_text)})
    citations: list[Citation] = []
    for idx in used_indices:
        if 1 <= idx <= len(chunks):
            chunk = chunks[idx - 1]
            citations.append(
                Citation(
                    index=idx,
                    source_uri=chunk.source_uri,
                    title=chunk.title,
                    snippet=chunk.text[:240] if chunk.text else None,
                )
            )
    return citations
