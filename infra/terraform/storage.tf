locals {
  staging_bucket_name = coalesce(
    var.staging_bucket_name,
    "${var.project_id}-${var.profile}-staging",
  )
}

# Staging bucket for raw documents (web/Drive exports) imported into the corpus.
resource "google_storage_bucket" "staging" {
  name                        = local.staging_bucket_name
  project                     = var.project_id
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = false
  labels                      = var.labels

  versioning {
    enabled = true
  }

  depends_on = [google_project_service.enabled]
}
