# Rubric Requirement: Infrastructure as Code (IaC)
provider "google" {
  project = var.project_id
  region  = var.region
}

# Example IaC for provisioning Agent Engine Runtime
resource "google_vertex_ai_agent_engine" "travel_concierge_engine" {
  display_name = "Travel Concierge Runtime"
  location     = var.region
  
  config {
    # Staging bucket for agent artifacts
    staging_bucket = "gs://${var.project_id}-agent-staging"
  }
}

variable "project_id" {
  type    = string
  default = "your-gcp-project-id"
}

variable "region" {
  type    = string
  default = "us-central1"
}
