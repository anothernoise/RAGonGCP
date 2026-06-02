"""In-memory fake backend — no GCP required.

Used by unit tests and for local development (`RAGONGCP_BACKEND=fake`). It
implements both the Retriever and Ingestor ports with a trivial keyword overlap
score so the full pipeline and API can run end-to-end offline.
"""

from __future__ import annotations

from ragongcp.domain.models import Chunk, Document, Query


def _score(query: str, text: str) -> float:
    """Jaccard-ish keyword overlap; good enough to order fake results."""
    q = {w for w in query.lower().split() if len(w) > 2}
    t = {w for w in text.lower().split() if len(w) > 2}
    if not q or not t:
        return 0.0
    return len(q & t) / len(q | t)


class FakeBackend:
    """Implements Retriever + Ingestor against an in-memory list of documents."""

    def __init__(self, top_k: int = 8, seed: list[Document] | None = None) -> None:
        self.top_k = top_k
        self._docs: list[Document] = list(seed or _default_seed())

    def ensure_corpus(self) -> str:
        return "fake://corpus"

    def upsert(self, documents: list[Document]) -> int:
        self._docs.extend(documents)
        return len(documents)

    def retrieve(self, query: Query) -> list[Chunk]:
        k = query.top_k or self.top_k
        scored = [
            Chunk(
                text=str(doc.metadata.get("text", doc.title or doc.uri)),
                source_uri=doc.uri,
                title=doc.title,
                score=_score(query.text, str(doc.metadata.get("text", doc.title or ""))),
            )
            for doc in self._docs
        ]
        scored.sort(key=lambda c: c.score, reverse=True)
        return [c for c in scored[:k] if c.score > 0] or scored[:1]


def _default_seed() -> list[Document]:
    """A tiny BC-real-estate-flavoured corpus so demos return something sensible."""
    return [
        Document(
            uri="https://www.bcfsa.ca/disclosure-of-representation",
            title="Disclosure of Representation in Trading Services",
            metadata={
                "text": (
                    "In British Columbia, a real estate licensee must provide the "
                    "Disclosure of Representation in Trading Services form to a "
                    "consumer at the earliest reasonable opportunity, explaining the "
                    "duties owed to clients versus unrepresented parties."
                )
            },
        ),
        Document(
            uri="https://www.bclaws.gov.bc.ca/resa/agency-duties",
            title="Real Estate Services Act — Agent Duties",
            metadata={
                "text": (
                    "Under the Real Estate Services Act, a brokerage and its "
                    "licensees owe fiduciary duties to their clients, including "
                    "loyalty, full disclosure of conflicts, confidentiality, and "
                    "acting in the client's best interest."
                )
            },
        ),
    ]
