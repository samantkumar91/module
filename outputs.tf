output "instance_metadata_function_url" {
  value       = module.instance_metadata_function_deployment.https_trigger_url
  description = "URL of Instance metadata report Cloud Function."
}