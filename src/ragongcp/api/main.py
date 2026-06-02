"""FastAPI app factory + DI wiring.

`create_app` resolves config and builds the RagService once, storing it on
app.state so routes can use it. Run locally with:

    uvicorn ragongcp.api.main:app --reload
    # or: python -m ragongcp.api.main
"""

from __future__ import annotations

from fastapi import FastAPI

from ragongcp.api.routes import router
from ragongcp.config import ProfileConfig, Settings, get_profile, get_settings
from ragongcp.pipeline.rag_service import RagService, build_default


def create_app(
    settings: Settings | None = None,
    profile: ProfileConfig | None = None,
    service: RagService | None = None,
) -> FastAPI:
    settings = settings or get_settings()
    profile = profile or get_profile(settings)

    app = FastAPI(
        title="RAGonGCP",
        version="0.1.0",
        description="Reusable enterprise RAG accelerator on Vertex AI / Gemini.",
    )
    app.state.settings = settings
    app.state.profile = profile
    # `service` is injectable for tests; otherwise built lazily from config on first use.
    app.state.service = service or _LazyService(settings, profile)
    app.include_router(router)
    return app


class _LazyService:
    """Defers backend construction until the first request that needs it.

    Lets `/healthz` and app import succeed even if (e.g.) GCP creds aren't set,
    while `/query` and `/ingest` build the real service on demand.
    """

    def __init__(self, settings: Settings, profile: ProfileConfig) -> None:
        self._settings = settings
        self._profile = profile
        self._real: RagService | None = None

    def _resolve(self) -> RagService:
        if self._real is None:
            self._real = build_default(self._settings, self._profile)
        return self._real

    def __getattr__(self, name: str):
        return getattr(self._resolve(), name)


app = create_app()


def main() -> None:  # pragma: no cover
    import uvicorn

    uvicorn.run("ragongcp.api.main:app", host="0.0.0.0", port=8080, reload=False)


if __name__ == "__main__":  # pragma: no cover
    main()
