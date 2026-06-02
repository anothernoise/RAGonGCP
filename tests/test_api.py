from fastapi.testclient import TestClient

from ragongcp.adapters.fake import FakeBackend
from ragongcp.api.main import create_app
from ragongcp.config import ProfileConfig, Settings
from ragongcp.generation.echo import EchoGenerator
from ragongcp.pipeline.rag_service import RagService


def _client() -> TestClient:
    profile = ProfileConfig()
    profile.backend = "fake"
    settings = Settings(profile="bc_real_estate", backend="fake")
    service = RagService(retriever=FakeBackend(), generator=EchoGenerator())
    app = create_app(settings=settings, profile=profile, service=service)
    return TestClient(app)


def test_healthz():
    resp = _client().get("/healthz")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["backend"] == "fake"


def test_query_endpoint_returns_answer_with_citations():
    resp = _client().post("/query", json={"question": "agent duties under RESA"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["answer"]
    assert len(body["citations"]) >= 1


def test_ingest_endpoint():
    resp = _client().post(
        "/ingest",
        json={"documents": [{"uri": "gs://b/x.txt", "title": "X", "metadata": {"text": "policy"}}]},
    )
    assert resp.status_code == 200
    assert resp.json()["imported"] == 1
