locals {
  role_permissions = ["bigquery.datasets.get", "bigquery.jobs.create", "bigquery.tables.create", "bigquery.tables.get", "bigquery.tables.update",
    "bigquery.tables.updateData", "resourcemanager.projects.get", "storage.buckets.get", "storage.objects.create",
    "storage.objects.delete", "storage.objects.get", "storage.objects.list", "storage.objects.update",
    "bigquery.tables.delete", "bigquery.datasets.getIamPolicy", "bigquery.datasets.update",
    "bigquery.datasets.updateTag", "bigquery.jobs.get", "bigquery.jobs.list", "bigquery.readsessions.create",
    "bigquery.readsessions.getData", "bigquery.readsessions.update", "bigquery.reservationAssignments.list",
    "bigquery.reservationAssignments.search", "bigquery.reservations.get", "bigquery.reservations.list",
    "bigquery.routines.get", "bigquery.routines.list", "bigquery.savedqueries.get", "bigquery.savedqueries.list",
    "bigquery.tables.export", "bigquery.tables.getData", "bigquery.tables.getIamPolicy", "bigquery.tables.list",
  "bigquery.tables.setCategory", "bigquery.tables.updateTag", "bigquery.transfers.get", ]

  folder_roles = ["roles/compute.viewer", "roles/resourcemanager.folderViewer"]

  name_acct_pairs = flatten([
    for folder in var.gcp_folder_list : [
      for folder_role in local.folder_roles : {
        folder     = folder
        role       = folder_role
        svc_acc_nm = "serviceAccount:${module.instance_metadata_function_deployment.email}"
      }
    ]
  ])

  cloud_function_root = abspath(path.module)
}

data "archive_file" "instance_metadata" {
  output_path = "${local.cloud_function_root}/cloudFunctions/${var.service_name}/${var.service_name}.zip"
  source_dir  = "${local.cloud_function_root}/cloudFunctions/${var.service_name}"
  type        = "zip"
}

module "instance_metadata_function_deployment" {
  source                            = "git@github.com:GLB-CES-PublicCloud-Google/dcs-gcp-code.git//modules/scheduledFunction?ref=plan"
  project                           = var.project
  region                            = var.region
  service_name                      = var.service_name
  environment                       = var.environment
  entry_point                       = var.entry_point
  location                          = var.bucket_location
  function_vars                     = merge(var.function_vars, { "TABLE_NAME" : var.service_name, "DATASET_ID" : var.dataset_id, "BUCKET_NAME" : module.instance_metadata_function_deployment.bucket_name, "BQ_PROJECT" : var.project, "PARENT_FOLDERS" : join(", ", var.gcp_folder_list), "BQ_RETENTION" : var.bq_reports_retention_time, })
  schedule                          = var.schedule
  schedule_request_body             = var.schedule_request_body
  role_permissions                  = local.role_permissions
  enable_default_scheduler_creation = var.enable_default_scheduler_creation
  cloud_function_root               = local.cloud_function_root

  depends_on = [data.archive_file.instance_metadata]
}

resource "google_folder_iam_member" "admin" {
  count  = length(local.name_acct_pairs)
  folder = local.name_acct_pairs[count.index].folder
  role   = local.name_acct_pairs[count.index].role
  member = local.name_acct_pairs[count.index].svc_acc_nm

  depends_on = [module.instance_metadata_function_deployment]
}
