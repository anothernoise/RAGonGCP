"""Thin import shim for the Vertex AI RAG Engine SDK.

The RAG module moved from `vertexai.preview.rag` to the GA `vertexai.rag`
namespace across SDK versions. Import lazily and tolerate both so the rest of
the adapter doesn't care which is installed. Raises a clear error only when an
operation is actually invoked without the SDK present.
"""

from __future__ import annotations


def load_rag():
    """Return the `rag` module, preferring the GA namespace."""
    try:
        from vertexai import rag  # GA (newer SDK)

        return rag
    except Exception:  # pragma: no cover - depends on installed SDK version
        try:
            from vertexai.preview import rag  # preview (older SDK)

            return rag
        except Exception as exc:  # pragma: no cover
            raise ImportError(
                "Vertex AI RAG Engine SDK not available. Install "
                "'google-cloud-aiplatform>=1.71' and authenticate (ADC) to use "
                "the vertex_rag_engine backend."
            ) from exc


def load_vertexai():
    try:
        import vertexai

        return vertexai
    except Exception as exc:  # pragma: no cover
        raise ImportError(
            "vertexai is not installed. Install 'google-cloud-aiplatform>=1.71'."
        ) from exc
