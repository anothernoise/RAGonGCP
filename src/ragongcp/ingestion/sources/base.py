"""Ingestion source interface.

A Source turns a configured location (GCS prefix, Drive folder, web URLs) into a
list of `Document`s whose `uri` the active backend can import. Sources that pull
external content stage it to GCS first and return gs:// URIs.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ragongcp.config import Settings
from ragongcp.domain.models import Document


@runtime_checkable
class Source(Protocol):
    def collect(self, settings: Settings) -> list[Document]:
        """Discover/stage documents and return them as importable Documents."""
        ...
