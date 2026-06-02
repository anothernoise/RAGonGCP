"""RagService — orchestrates retrieve -> generate -> cite.

This is the application core. It depends only on the domain Protocols
(Retriever, Generator), so it is fully testable with fakes and works unchanged
across every backend. The factory in `build_default` wires concrete pieces from
config.
"""

from __future__ import annotations

from ragongcp.config import ProfileConfig, Settings, get_profile, get_settings
from ragongcp.domain.generator import Generator
from ragongcp.domain.models import Answer, Document, Query
from ragongcp.domain.retriever import Retriever


class RagService:
    def __init__(self, retriever: Retriever, generator: Generator) -> None:
        self.retriever = retriever
        self.generator = generator

    def query(self, text: str, top_k: int | None = None) -> Answer:
        chunks = self.retriever.retrieve(Query(text=text, top_k=top_k))
        return self.generator.generate(text, chunks)

    def ingest(self, documents: list[Document]) -> int:
        # The retriever doubles as the ingestor for our backends (both ports).
        self.retriever.ensure_corpus()  # type: ignore[attr-defined]
        return self.retriever.upsert(documents)  # type: ignore[attr-defined]


def build_generator(profile: ProfileConfig, settings: Settings) -> Generator:
    """Pick the generator matching the backend (echo for fake/offline, else Gemini)."""
    if profile.backend == "fake":
        from ragongcp.generation.echo import EchoGenerator

        return EchoGenerator()
    from ragongcp.generation.gemini import GeminiGenerator

    return GeminiGenerator(generation=profile.generation, settings=settings)


def build_default(
    settings: Settings | None = None, profile: ProfileConfig | None = None
) -> RagService:
    """Construct a RagService from the active environment + profile config."""
    from ragongcp.adapters.factory import build_retriever

    settings = settings or get_settings()
    profile = profile or get_profile(settings)
    retriever = build_retriever(profile, settings)
    generator = build_generator(profile, settings)
    return RagService(retriever=retriever, generator=generator)
