"""Vertex AI RAG Engine backend — the default retrieval/ingestion adapter.

Implements both the Retriever and Ingestor ports against a managed RagCorpus.
The corpus handles chunking, embedding, and the vector store; we just create it,
import GCS files into it, and run retrieval queries.

Docs: https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview
"""

from __future__ import annotations

from ragongcp.adapters.vertex_rag_engine import corpus as corpus_helpers
from ragongcp.adapters.vertex_rag_engine._sdk import load_rag, load_vertexai
from ragongcp.config import ProfileConfig, Settings
from ragongcp.domain.models import Chunk, Document, Query


class VertexRagEngineBackend:
    """Retriever + Ingestor backed by a Vertex AI RAG Engine corpus."""

    def __init__(self, profile: ProfileConfig, settings: Settings) -> None:
        self.profile = profile
        self.settings = settings
        self._corpus = None
        self._initialized = False

    # --- init / corpus -------------------------------------------------

    def _init_vertex(self) -> None:
        if self._initialized:
            return
        if not self.settings.project_id:
            raise RuntimeError(
                "RAGONGCP_PROJECT_ID is not set — required for the vertex_rag_engine backend."
            )
        vertexai = load_vertexai()
        vertexai.init(project=self.settings.project_id, location=self.settings.location)
        self._initialized = True

    def ensure_corpus(self) -> str:
        self._init_vertex()
        if self._corpus is None:
            self._corpus = corpus_helpers.ensure_corpus(self.profile.retrieval)
        return self._corpus.name

    # --- ingestion -----------------------------------------------------

    def upsert(self, documents: list[Document]) -> int:
        """Import documents (by GCS/Drive URI) into the corpus.

        Vertex RAG Engine imports from GCS or Google Drive URIs directly; the
        ingestion `sources` are responsible for staging raw content to GCS first.
        """
        self.ensure_corpus()
        rag = load_rag()

        paths = [doc.uri for doc in documents if doc.uri.startswith(("gs://", "https://drive."))]
        if not paths:
            return 0

        retrieval = self.profile.retrieval
        transformation_config = rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(
                chunk_size=retrieval.chunk_size,
                chunk_overlap=retrieval.chunk_overlap,
            )
        )
        rag.import_files(
            self._corpus.name,
            paths=paths,
            transformation_config=transformation_config,
        )
        return len(paths)

    # --- retrieval -----------------------------------------------------

    def retrieve(self, query: Query) -> list[Chunk]:
        self.ensure_corpus()
        rag = load_rag()
        retrieval = self.profile.retrieval

        retrieval_config = rag.RagRetrievalConfig(
            top_k=query.top_k or retrieval.top_k,
            filter=rag.RagRetrievalConfig.Filter(
                vector_distance_threshold=retrieval.vector_distance_threshold
            ),
        )
        response = rag.retrieval_query(
            rag_resources=[rag.RagResource(rag_corpus=self._corpus.name)],
            text=query.text,
            rag_retrieval_config=retrieval_config,
        )
        return _to_chunks(response)


def _to_chunks(response) -> list[Chunk]:
    """Normalize a RAG Engine retrieval response into domain Chunks."""
    contexts = getattr(getattr(response, "contexts", None), "contexts", None) or []
    chunks: list[Chunk] = []
    for ctx in contexts:
        source_uri = getattr(ctx, "source_uri", "") or getattr(ctx, "source_display_name", "")
        chunks.append(
            Chunk(
                text=getattr(ctx, "text", "") or "",
                source_uri=source_uri or "unknown",
                title=getattr(ctx, "source_display_name", None),
                score=float(getattr(ctx, "score", 0.0) or 0.0),
            )
        )
    return chunks
