"""Web source — fetch public governance resources and stage them to GCS.

Used for external BC real estate governance content (BCFSA, BC Laws, BCREA).
Enforces a domain allowlist so only sanctioned sources are fetched, then uploads
each page/PDF to the staging bucket and returns gs:// URIs for the corpus import.
"""

from __future__ import annotations

import hashlib
from urllib.parse import urlparse

from ragongcp.config import Settings
from ragongcp.domain.models import Document


def host_allowed(url: str, allowlist: list[str]) -> bool:
    """True if the URL's host exactly matches an allowlisted domain."""
    host = (urlparse(url).hostname or "").lower()
    return host in {d.lower() for d in allowlist}


def _object_name(url: str) -> str:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    path = urlparse(url).path.rsplit("/", 1)[-1] or "index"
    if "." not in path:
        path += ".html"
    return f"web/{digest}-{path}"


class WebSource:
    def __init__(self, urls: list[str], allowlist: list[str]) -> None:
        self.urls = urls
        self.allowlist = allowlist

    def collect(self, settings: Settings) -> list[Document]:
        if not settings.staging_bucket:
            raise ValueError(
                "RAGONGCP_STAGING_BUCKET must be set to stage web content for ingestion."
            )

        blocked = [u for u in self.urls if not host_allowed(u, self.allowlist)]
        if blocked:
            raise ValueError(
                f"Refusing to fetch URLs outside the allowlist {self.allowlist}: {blocked}"
            )

        import httpx
        from google.cloud import storage

        client = storage.Client(project=settings.project_id or None)
        bucket = client.bucket(settings.staging_bucket)

        docs: list[Document] = []
        with httpx.Client(timeout=30, follow_redirects=True) as http:
            for url in self.urls:
                resp = http.get(url)
                resp.raise_for_status()
                content_type = resp.headers.get("content-type", "text/html").split(";")[0]
                object_name = _object_name(url)
                blob = bucket.blob(object_name)
                blob.upload_from_string(resp.content, content_type=content_type)
                docs.append(
                    Document(
                        uri=f"gs://{settings.staging_bucket}/{object_name}",
                        title=url,
                        mime_type=content_type,
                        metadata={"origin_url": url},
                    )
                )
        return docs
