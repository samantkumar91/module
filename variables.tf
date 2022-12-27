variable "project" {
  description = "Name of the project"
  type        = string
}

variable "region" {
  description = "Name of default region"
  type        = string
}

variable "organization_id" {
  type        = string
  description = "ID of the organization"
}

variable "service_name" {
  description = "Name of service to be deployed"
  type        = string
  default     = "instanceMetadata"
}

variable "environment" {
  type        = string
  description = "Environment deployed"
  default     = ""
}

variable "entry_point" {
  type        = string
  description = "Function entry_point - which function should be triggered by defualt"
  default     = "main"
}

variable "function_vars" {
  description = "All environment variables for function to be deployed"
  type        = map(any)
  default     = {}
}

variable "schedule" {
  description = "cron style schedule"
  type        = string
  default     = "0 */2 * * *"
}

variable "enable_default_scheduler_creation" {
  description = "Set true to deploy Cloud schedule for Cloud Function."
  type        = bool
  default     = true
}

variable "dataset_id" {
  type        = string
  description = "Reporting dataset ID."
  default     = "dcs_reports"
}

variable "gcp_folder_list" {
  type        = list(string)
  description = "List of folders where to apply the roles and which contain projects for reports."
}

variable "schedule_request_body" {
  description = "Payload to be sent via schedule."
  type        = string
  default     = ""
}

variable "bucket_location" {
  description = "Storage Bucket location"
  type        = string
  default     = "US"
}

variable "bq_reports_retention_time" {
  description = "Number of MONTHS to keep the data in BigQuery"
  type        = number
  default     = 13
}
