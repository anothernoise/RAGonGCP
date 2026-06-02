"""API routes: /query, /ingest, /healthz.

The RagService is resolved from app state (set up in main.create_app), so the
same routes work against any backend including the offline fake.
"""

from __future__ import annotations

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
    try:
        answer = service.query(body.question, top_k=body.top_k)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:  # surface backend/config errors as 502
        raise HTTPException(status_code=502, detail=f"Retrieval/generation failed: {exc}") from exc
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
