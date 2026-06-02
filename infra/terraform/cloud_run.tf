# Cloud Run service for the FastAPI app. Disabled by default until an image
# exists (set deploy_cloud_run = true and provide container_image).
resource "google_cloud_run_v2_service" "api" {
  count    = var.deploy_cloud_run ? 1 : 0
  name     = "${local.name_prefix}-api"
  project  = var.project_id
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.runtime.email

    containers {
      image = var.container_image

      env {
        name  = "RAGONGCP_PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "RAGONGCP_LOCATION"
        value = var.region
      }
      env {
        name  = "RAGONGCP_PROFILE"
        value = var.profile
      }
      env {
        name  = "RAGONGCP_STAGING_BUCKET"
        value = google_storage_bucket.staging.name
      }
      env {
        name  = "RAGONGCP_COST_TRACKING_ENABLED"
        value = lower(tostring(var.enable_cost_tracking))
      }
      env {
        name  = "RAGONGCP_COST_TRACKING_SINK"
        value = var.cost_tracking_sink
      }
      env {
        name  = "RAGONGCP_COST_TRACKING_BQ_DATASET"
        value = var.cost_tracking_bq_dataset
      }
      env {
        name  = "RAGONGCP_COST_TRACKING_BQ_TABLE"
        value = var.cost_tracking_bq_table
      }

      ports {
        container_port = 8080
      }
    }
  }

  depends_on = [google_project_service.enabled]
}
