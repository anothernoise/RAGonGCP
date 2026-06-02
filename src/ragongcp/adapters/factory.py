"""Backend factory — selects the retriever/ingestor pair from config.

This is the single place that knows about concrete backends. Everything else
depends only on the domain Protocols. Adding a new backend = add a branch here.
"""

from __future__ import annotations

from ragongcp.config import ProfileConfig, Settings
from ragongcp.domain.ingestor import Ingestor
from ragongcp.domain.retriever import Retriever


class UnknownBackendError(ValueError):
    pass


def build_retriever(profile: ProfileConfig, settings: Settings) -> Retriever:
    return _build(profile, settings)


def build_ingestor(profile: ProfileConfig, settings: Settings) -> Ingestor:
    return _build(profile, settings)


def _build(profile: ProfileConfig, settings: Settings):
    backend = profile.backend

    if backend == "fake":
        from ragongcp.adapters.fake import FakeBackend

        return FakeBackend(top_k=profile.retrieval.top_k)

    if backend == "vertex_rag_engine":
        # Imported lazily so the package (and tests) load without GCP libs/creds.
        from ragongcp.adapters.vertex_rag_engine.client import VertexRagEngineBackend

        return VertexRagEngineBackend(profile=profile, settings=settings)

    if backend == "vertex_search":
        from ragongcp.adapters.vertex_search.client import VertexSearchBackend

        return VertexSearchBackend(profile=profile, settings=settings)

    if backend == "custom_vector":
        from ragongcp.adapters.custom_vector.client import CustomVectorBackend

        return CustomVectorBackend(profile=profile, settings=settings)

    raise UnknownBackendError(
        f"Unknown backend '{backend}'. "
        "Expected one of: vertex_rag_engine, vertex_search, custom_vector, fake."
    )
