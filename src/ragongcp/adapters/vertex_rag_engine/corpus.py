"""RagCorpus lifecycle helpers for the Vertex AI RAG Engine backend."""

from __future__ import annotations

from ragongcp.adapters.vertex_rag_engine._sdk import load_rag
from ragongcp.config import RetrievalConfig


def find_corpus(display_name: str):
    """Return the existing corpus with `display_name`, or None."""
    rag = load_rag()
    for corpus in rag.list_corpora():
        if getattr(corpus, "display_name", None) == display_name:
            return corpus
    return None


def ensure_corpus(retrieval: RetrievalConfig):
    """Get-or-create a RagCorpus configured with the profile's embedding model.

    Returns the corpus resource (its `.name` is the corpus id used elsewhere).
    """
    rag = load_rag()

    existing = find_corpus(retrieval.corpus_display_name)
    if existing is not None:
        return existing

    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model=f"publishers/google/models/{retrieval.embedding_model}",
        )
    )
    backend_config = rag.RagVectorDbConfig(rag_embedding_model_config=embedding_model_config)

    return rag.create_corpus(
        display_name=retrieval.corpus_display_name,
        backend_config=backend_config,
    )
