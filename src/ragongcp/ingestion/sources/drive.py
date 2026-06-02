"""Google Workspace (Drive) source.

Lists files in a shared Drive folder so they can be imported into the corpus.
Vertex AI RAG Engine can import Google Drive resource URLs directly, so by
default we return the Drive file URLs (no copy needed).

Auth: uses Application Default Credentials. For Workspace-wide access, run the
service account with domain-wide delegation and the Drive read-only scope; share
the target folder with the service account. This POC keeps the wiring minimal.
"""

from __future__ import annotations

from ragongcp.config import Settings
from ragongcp.domain.models import Document

_DRIVE_SCOPE = "https://www.googleapis.com/auth/drive.readonly"


class DriveSource:
    def __init__(self, folder_id: str) -> None:
        self.folder_id = folder_id

    def collect(self, settings: Settings) -> list[Document]:
        if not self.folder_id or self.folder_id.startswith("REPLACE_"):
            raise ValueError(
                "Drive source folder_id is not configured. Set it in the profile "
                "yaml (ingestion.sources[].folder_id)."
            )

        import google.auth
        from googleapiclient.discovery import build

        credentials, _ = google.auth.default(scopes=[_DRIVE_SCOPE])
        service = build("drive", "v3", credentials=credentials)

        docs: list[Document] = []
        page_token = None
        query = f"'{self.folder_id}' in parents and trashed = false"
        while True:
            resp = (
                service.files()
                .list(
                    q=query,
                    fields="nextPageToken, files(id, name, mimeType, webViewLink)",
                    pageToken=page_token,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                )
                .execute()
            )
            for f in resp.get("files", []):
                docs.append(
                    Document(
                        uri=f.get("webViewLink") or f"https://drive.google.com/file/d/{f['id']}",
                        title=f.get("name"),
                        mime_type=f.get("mimeType", "application/octet-stream"),
                        metadata={"drive_file_id": f["id"]},
                    )
                )
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        return docs
