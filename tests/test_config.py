from ragongcp.config import get_profile, load_profile
from ragongcp.config import Settings


def test_profile_inherits_default_and_overrides():
    profile = load_profile("bc_real_estate")
    # Overridden in bc_real_estate.yaml
    assert profile.retrieval.corpus_display_name == "ragongcp-bc-real-estate"
    assert profile.retrieval.top_k == 10
    # Inherited from default.yaml (not set in the profile)
    assert profile.retrieval.embedding_model == "text-embedding-005"
    assert profile.backend == "vertex_rag_engine"


def test_unknown_profile_falls_back_to_defaults():
    profile = load_profile("does_not_exist")
    assert profile.backend == "vertex_rag_engine"
    assert profile.retrieval.top_k == 8


def test_env_backend_override():
    settings = Settings(profile="bc_real_estate", backend="fake")
    profile = get_profile(settings)
    assert profile.backend == "fake"
