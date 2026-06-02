import pytest

from ragongcp.adapters.factory import UnknownBackendError, build_retriever
from ragongcp.config import ProfileConfig, Settings


def _profile(backend: str) -> ProfileConfig:
    p = ProfileConfig()
    p.backend = backend
    return p


def test_factory_builds_fake_backend():
    backend = build_retriever(_profile("fake"), Settings())
    assert backend.ensure_corpus() == "fake://corpus"


def test_factory_unknown_backend_raises():
    with pytest.raises(UnknownBackendError):
        build_retriever(_profile("nope"), Settings())


def test_stub_backends_raise_not_implemented():
    for backend in ("vertex_search", "custom_vector"):
        be = build_retriever(_profile(backend), Settings())
        with pytest.raises(NotImplementedError):
            be.ensure_corpus()
