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


def test_cost_tracking_settings_defaults():
    settings = Settings()
    assert settings.cost_tracking_enabled is False
    assert settings.cost_tracking_sink == "log"
    assert settings.cost_tracking_bq_dataset == ""
    assert settings.cost_tracking_bq_table == "rag_cost_events"


def test_cost_tracking_settings_overrides():
    settings = Settings(
        cost_tracking_enabled=True,
        cost_tracking_sink="bigquery",
        cost_tracking_bq_dataset="finops",
        cost_tracking_bq_table="cost_events",
    )
    assert settings.cost_tracking_enabled is True
    assert settings.cost_tracking_sink == "bigquery"
    assert settings.cost_tracking_bq_dataset == "finops"
    assert settings.cost_tracking_bq_table == "cost_events"
