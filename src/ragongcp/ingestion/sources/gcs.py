"""GCS source — list objects under a bucket/prefix as importable Documents.

This is the simplest, most reliable source: point the corpus at content already
in Cloud Storage. Other sources (Drive, web) stage into GCS and reuse this path.
"""

from __future__ import annotations

import mimetypes

from ragongcp.config import Settings
from ragongcp.domain.models import Document


class GcsSource:
    def __init__(self, bucket: str, prefix: str = "") -> None:
        self.bucket = bucket
        self.prefix = prefix

    def collect(self, settings: Settings) -> list[Document]:
        from google.cloud import storage  # imported lazily

        client = storage.Client(project=settings.project_id or None)
        docs: list[Document] = []
        for blob in client.list_blobs(self.bucket, prefix=self.prefix):
            if blob.name.endswith("/"):
                continue
            mime = blob.content_type or mimetypes.guess_type(blob.name)[0] or "text/plain"
            docs.append(
                Document(
                    uri=f"gs://{self.bucket}/{blob.name}",
                    title=blob.name.rsplit("/", 1)[-1],
                    mime_type=mime,
                )
            )
        return docs
