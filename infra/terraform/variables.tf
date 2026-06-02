variable "project_id" {
  type        = string
  description = "GCP project ID to deploy into."
}

variable "region" {
  type        = string
  description = "GCP region for regional resources (Cloud Run, buckets)."
  default     = "us-central1"
}

variable "profile" {
  type        = string
  description = "RAGonGCP use-case profile (drives resource naming + RAGONGCP_PROFILE)."
  default     = "bc_real_estate"
}

variable "staging_bucket_name" {
  type        = string
  description = "Globally-unique name for the document staging bucket. Defaults to <project>-<profile>-staging."
  default     = ""
}

variable "container_image" {
  type        = string
  description = "Container image for the Cloud Run API service (e.g. REGION-docker.pkg.dev/PROJECT/repo/ragongcp:tag)."
  default     = ""
}

variable "deploy_cloud_run" {
  type        = bool
  description = "Whether to deploy the Cloud Run service. Set false to provision data/IAM only."
  default     = false
}

variable "labels" {
  type        = map(string)
  description = "Labels applied to created resources."
  default = {
    app = "ragongcp"
  }
}
