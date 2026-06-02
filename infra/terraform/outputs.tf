output "staging_bucket" {
  description = "Name of the document staging bucket."
  value       = google_storage_bucket.staging.name
}

output "runtime_service_account" {
  description = "Email of the runtime service account."
  value       = google_service_account.runtime.email
}

output "cloud_run_url" {
  description = "URL of the deployed Cloud Run service (empty if not deployed)."
  value       = var.deploy_cloud_run ? google_cloud_run_v2_service.api[0].uri : ""
}
