# Enable the Google Cloud APIs the accelerator needs.
locals {
  services = [
    "aiplatform.googleapis.com",     # Vertex AI (RAG Engine, Gemini, embeddings)
    "storage.googleapis.com",        # GCS staging bucket
    "run.googleapis.com",            # Cloud Run API service
    "artifactregistry.googleapis.com", # container images for Cloud Run
    "drive.googleapis.com",          # Google Workspace Drive ingestion
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
  ]
}

resource "google_project_service" "enabled" {
  for_each                   = toset(local.services)
  project                    = var.project_id
  service                    = each.value
  disable_on_destroy         = false
  disable_dependent_services = false
}
