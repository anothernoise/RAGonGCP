"""Ingestion CLI — stage a profile's sources and import them into the corpus.

    python -m ragongcp.ingestion.run --profile bc_real_estate
    python -m ragongcp.ingestion.run --gcs-bucket my-bucket --gcs-prefix docs/

Builds sources from the profile's `ingestion.sources`, collects Documents from
each, then upserts them into the active backend's corpus.
"""

from __future__ import annotations

import argparse

from ragongcp.config import ProfileConfig, Settings, get_profile, get_settings
from ragongcp.domain.models import Document
from ragongcp.ingestion.sources.base import Source


def build_sources(profile: ProfileConfig, extra: list[Source] | None = None) -> list[Source]:
    """Instantiate Source objects from the profile's ingestion config."""
    from ragongcp.ingestion.sources.drive import DriveSource
    from ragongcp.ingestion.sources.gcs import GcsSource
    from ragongcp.ingestion.sources.web import WebSource

    sources: list[Source] = list(extra or [])
    allowlist = profile.ingestion.web_allowlist
    for spec in profile.ingestion.sources:
        kind = spec.get("type")
        if kind == "gcs":
            sources.append(GcsSource(bucket=spec["bucket"], prefix=spec.get("prefix", "")))
        elif kind == "drive":
            sources.append(DriveSource(folder_id=spec["folder_id"]))
        elif kind == "web":
            sources.append(WebSource(urls=spec.get("urls", []), allowlist=allowlist))
        else:
            raise ValueError(f"Unknown ingestion source type: {kind!r}")
    return sources


def collect_documents(sources: list[Source], settings: Settings) -> list[Document]:
    docs: list[Document] = []
    for source in sources:
        docs.extend(source.collect(settings))
    return docs


def run(settings: Settings, profile: ProfileConfig, extra: list[Source] | None = None) -> int:
    from ragongcp.adapters.factory import build_ingestor

    sources = build_sources(profile, extra=extra)
    documents = collect_documents(sources, settings)
    print(f"Collected {len(documents)} document(s) from {len(sources)} source(s).")

    ingestor = build_ingestor(profile, settings)
    corpus = ingestor.ensure_corpus()
    imported = ingestor.upsert(documents)
    print(f"Imported {imported} document(s) into corpus: {corpus}")
    return imported


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents into a RAGonGCP corpus.")
    parser.add_argument("--profile", help="Override RAGONGCP_PROFILE for this run.")
    parser.add_argument("--gcs-bucket", help="Ad-hoc GCS bucket source.")
    parser.add_argument("--gcs-prefix", default="", help="Prefix for the ad-hoc GCS source.")
    args = parser.parse_args()

    settings = get_settings()
    if args.profile:
        settings = Settings(**{**settings.model_dump(), "profile": args.profile})
    profile = get_profile(settings)

    extra: list[Source] = []
    if args.gcs_bucket:
        from ragongcp.ingestion.sources.gcs import GcsSource

        extra.append(GcsSource(bucket=args.gcs_bucket, prefix=args.gcs_prefix))

    run(settings, profile, extra=extra)


if __name__ == "__main__":  # pragma: no cover
    main()
