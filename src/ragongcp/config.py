"""Configuration: environment settings + layered YAML profile loading.

Two layers:
  1. `Settings` — environment-driven (project, location, profile, secrets).
  2. A YAML profile (`config/<profile>.yaml`) deep-merged over `config/default.yaml`,
     giving per-use-case retrieval/generation/ingestion config.

Anything an operator might change per deployment lives in env or yaml — never
hardcoded in code. `RAGONGCP_PROFILE=bc_real_estate` switches the whole use case.
"""

from __future__ import annotations

import copy
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Repo root = three levels up from this file (src/ragongcp/config.py).
REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"


class Settings(BaseSettings):
    """Environment-driven settings (prefix RAGONGCP_)."""

    model_config = SettingsConfigDict(env_prefix="RAGONGCP_", env_file=".env", extra="ignore")

    project_id: str = ""
    location: str = "us-central1"
    profile: str = "bc_real_estate"
    staging_bucket: str = ""
    # Optional explicit backend override; when empty, the profile yaml decides.
    backend: str = ""
    # Optional FinOps/cost-tracking controls.
    cost_tracking_enabled: bool = False
    cost_tracking_sink: Literal["log", "bigquery"] = "log"
    cost_tracking_bq_dataset: str = ""
    cost_tracking_bq_table: str = "rag_cost_events"


class RetrievalConfig(BaseModel):
    corpus_display_name: str = "ragongcp-default"
    embedding_model: str = "text-embedding-005"
    top_k: int = 8
    vector_distance_threshold: float = 0.5
    chunk_size: int = 1024
    chunk_overlap: int = 200


class GenerationConfig(BaseModel):
    model: str = "gemini-2.0-flash-001"
    temperature: float = 0.2
    max_output_tokens: int = 2048
    system_prompt: str = ""


class IngestionConfig(BaseModel):
    sources: list[dict[str, Any]] = Field(default_factory=list)
    web_allowlist: list[str] = Field(default_factory=list)


class ProfileConfig(BaseModel):
    """Fully-resolved use-case configuration (default.yaml + profile overlay)."""

    backend: str = "vertex_rag_engine"
    retrieval: RetrievalConfig = Field(default_factory=RetrievalConfig)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
    ingestion: IngestionConfig = Field(default_factory=IngestionConfig)


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge `overlay` onto `base` (overlay wins on scalar/list keys)."""
    result = copy.deepcopy(base)
    for key, value in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_profile(profile: str, config_dir: Path = CONFIG_DIR) -> ProfileConfig:
    """Load `config/<profile>.yaml` merged over `config/default.yaml`."""
    base = _load_yaml(config_dir / "default.yaml")
    overlay = _load_yaml(config_dir / f"{profile}.yaml")
    merged = _deep_merge(base, overlay)
    return ProfileConfig(**merged)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def get_profile(settings: Settings | None = None) -> ProfileConfig:
    """Resolve the active profile, applying an env backend override if set."""
    settings = settings or get_settings()
    profile = load_profile(settings.profile)
    if settings.backend:
        profile.backend = settings.backend
    return profile
