"""API routes: /query, /ingest, /healthz.

The RagService is resolved from app state (set up in main.create_app), so the
same routes work against any backend including the offline fake.
"""

from __future__ import annotations

import time
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from ragongcp.api.schemas import (
    HealthResponse,
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
)

router = APIRouter()


@router.get("/healthz", response_model=HealthResponse)
def healthz(request: Request) -> HealthResponse:
    state = request.app.state
    return HealthResponse(
        status="ok",
        profile=state.settings.profile,
        backend=state.profile.backend,
    )


@router.post("/query", response_model=QueryResponse)
def query(request: Request, body: QueryRequest) -> QueryResponse:
    service = request.app.state.service
    started = time.perf_counter()
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    try:
        answer = service.query(body.question, top_k=body.top_k)
    except NotImplementedError as exc:
        _record_cost_event(
            request,
            {
                "event_type": "query",
                "request_id": request_id,
                "status": "not_implemented",
                "error_type": type(exc).__name__,
                "duration_ms": int((time.perf_counter() - started) * 1000),
            },
        )
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:  # surface backend/config errors as 502
        _record_cost_event(
            request,
            {
                "event_type": "query",
                "request_id": request_id,
                "status": "error",
                "error_type": type(exc).__name__,
                "duration_ms": int((time.perf_counter() - started) * 1000),
            },
        )
        raise HTTPException(status_code=502, detail=f"Retrieval/generation failed: {exc}") from exc

    _record_cost_event(
        request,
        {
            "event_type": "query",
            "request_id": request_id,
            "status": "ok",
            "profile": request.app.state.settings.profile,
            "backend": request.app.state.profile.backend,
            "model": answer.model,
            "top_k": body.top_k,
            "question_chars": len(body.question),
            "answer_chars": len(answer.text),
            "citation_count": len(answer.citations),
            "retrieved_chunk_count": len(answer.chunks),
            "duration_ms": int((time.perf_counter() - started) * 1000),
            "usage": answer.usage,
        },
    )
    return QueryResponse(answer=answer.text, citations=answer.citations, model=answer.model)


@router.post("/ingest", response_model=IngestResponse)
def ingest(request: Request, body: IngestRequest) -> IngestResponse:
    service = request.app.state.service
    try:
        imported = service.ingest(body.documents)
        corpus = service.retriever.ensure_corpus()  # type: ignore[attr-defined]
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Ingestion failed: {exc}") from exc
    return IngestResponse(imported=imported, corpus=corpus)


def _record_cost_event(request: Request, event: dict[str, Any]) -> None:
    tracker = getattr(request.app.state, "cost_tracker", None)
    if tracker is None:
        return
    try:
        tracker.record_query(event)
    except Exception:
        # Observability must never break request serving.
        return
