# Instance metadata report

This service enables the functionality to generate Instance metadata report. The following components will be deployed:

- Cloud storage bucket with Cloud Function package,
- Instance metadata Cloud Function,
- custom role on the project level and roles on folders level,
- scheduler.

Zip archive will also be created automatically containing all files from the `cloudFunctions/instanceMetadata` directory.

**NOTE:** This service requires the reporting to be enabled, as BigQuery Dataset and App Engine application need to be created beforehand. If this service is used as intended (during DCS deployment), please set the `enable_reporting` and `gen_reporting_create_app_engine` variables to `true`. Otherwise manual steps are needed – the Dataset creation and App Engine enablement.

## Usage example

```
module "instance_metadata_report" {
    source = "git@github.com:GLB-CES-PublicCloud-Google/dcs-gcp-code.git//services/reportingInstanceMetadata?ref=plan"
    count                       = var.deploy_instance_metadata_report ? 1 : 0
    project                     = module.basic_landing_zone.tooling_project_id
    organization_id             = var.organization_id
    region                      = var.gen_reporting_region
    dataset_id                  = var.gen_reporting_dataset_id
    gcp_folder_list             = var.gcp_folder_list
}

```

## Providers

| Name | Version |
|------|---------|
| terraform | >= 0.13 |
| google | >= 3.50 |
| archive | 2.2.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| deploy_instance_metadata_report | If set to true the instance metadata report will be created. | `bool` | `false` | yes |
| gcp_folder_list | List of folders where to apply the roles and which contain projects for reports. | `list(string)` | n/a | yes |
| project | Google Project ID. | `string` | n/a | yes |
| region | Name of default region. | `string` | n/a | yes |
| organization_id | ID of the organization. | `string` | n/a | yes |
| service_name | Name of service to be deployed. | `string` | `instanceMetadata` | yes |
| environment | Environment deployed. | `string` | `""` | no |
| entry_point | Function entry_point - which function should be triggered by. | `string` | `main` | yes |
| function_vars | All environment variables for function to be deployed. | `map` | `{}` | yes |
| schedule | Cron style schedule. | `string` | `0 */2 * * *` | no |
| dataset_id | ID of the dataset used in reporting. | `string` | `dcs_reports` | yes |
| enable_default_scheduler_creation | Set true to deploy Cloud schedule for Cloud Function. | `bool` | `true` | no |
| schedule_request_body | Payload to be sent via schedule. | `string` | `""` | no |
| bucket_location | Storage Bucket location | `string` | `"US"` | no |

## Locals

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| folder_roles | List of roles given on folders. | `list(string)` | `["roles/compute.viewer","roles/resourcemanager.folderViewer"]` | yes |
| role_permissions | List of permissions for a custom role that will be created. | `list(string)` | long list - see `locals` definition in `main.tf` file | yes |


## Outputs

| Name | Description |
|------|-------------|
| instance_metadata_function_url | URL of Instance metadata report Cloud Function |