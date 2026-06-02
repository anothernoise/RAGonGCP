# Runtime service account for ingestion + the API service.
resource "google_service_account" "runtime" {
  project      = var.project_id
  account_id   = "${local.name_prefix}-sa"
  display_name = "RAGonGCP runtime (${var.profile})"
}

# Vertex AI access (RAG Engine, Gemini, embeddings).
resource "google_project_iam_member" "vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.runtime.email}"
}

# Read/write the staging bucket only (least privilege at the bucket scope).
resource "google_storage_bucket_iam_member" "staging_admin" {
  bucket = google_storage_bucket.staging.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.runtime.email}"
}
