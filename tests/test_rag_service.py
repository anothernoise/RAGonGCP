from ragongcp.adapters.fake import FakeBackend
from ragongcp.domain.models import Answer, Chunk, Document
from ragongcp.generation.echo import EchoGenerator
from ragongcp.pipeline.rag_service import RagService


class FakeGenerator:
    """Records the chunks it was given and returns a canned answer citing [1]."""

    def __init__(self):
        self.seen_chunks = None

    def generate(self, question, chunks):
        self.seen_chunks = chunks
        return Answer(text="Answer [1]", chunks=chunks, model="fake")


def _service(generator=None):
    return RagService(retriever=FakeBackend(), generator=generator or EchoGenerator())


def test_query_retrieves_then_generates():
    gen = FakeGenerator()
    service = _service(gen)
    answer = service.query("What are the agent duties under the Real Estate Services Act?")
    assert gen.seen_chunks is not None and len(gen.seen_chunks) > 0
    assert answer.model == "fake"


def test_echo_generator_produces_citations():
    service = _service()
    answer = service.query("disclosure of representation")
    assert answer.citations, "expected at least one citation"
    assert answer.citations[0].index == 1
    assert answer.citations[0].source_uri


def test_ingest_adds_documents():
    service = _service()
    imported = service.ingest(
        [Document(uri="gs://b/new.txt", title="New", metadata={"text": "brand new policy doc"})]
    )
    assert imported == 1
    # The new doc is now retrievable.
    answer = service.query("brand new policy")
    assert any("brand new" in c.snippet for c in answer.citations if c.snippet)


def test_no_context_yields_dont_know():
    gen = EchoGenerator()
    answer = gen.generate("anything", [])
    assert "don't know" in answer.text.lower()
    assert answer.citations == []


def test_chunk_model_roundtrip():
    chunk = Chunk(text="t", source_uri="gs://x", score=0.5)
    assert chunk.score == 0.5
