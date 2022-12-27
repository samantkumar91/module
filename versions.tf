terraform {

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 3.50"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.2.0"
    }
  }
}