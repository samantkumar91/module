## Introduction
This cloud function is use to create VM instance metadata reports. Reports will list the instance metadata.
## Inputs
- Service account with the mentioned permissions.
- Environment variables as below:

| Variable Name | Description |
|------|-------------|
| PARENT_FOLDERS | List of folders from which projects have to be used|
| BUCKET\_NAME | Name of the bucket |
| TABLE\_NAME | Name of table to be created OR Check existing table |
| DATASET\_ID | Existing bigquery dataset Id |
| BQ\_PROJECT | Name of project where bigquery dataset resides|


## Outputs
-  Creation of JSON file in the storage bucket
-  If not existing, creation of new table inside the bigquery dataset (should be existing dataset) with the records.

## Permissions
In order to execute this Cloud Function you must have a Service Account with the following:

a) Project level Custom role with following permissions:

- bigquery.jobs.create
- bigquery.tables.create
- bigquery.tables.get
- bigquery.tables.update
- bigquery.tables.updateData
- resourcemanager.projects.get
- storage.buckets.get
- storage.objects.create
- storage.objects.delete
- storage.objects.get
- storage.objects.list
- storage.objects.update

b) Folder level permissions:
- roles/compute.viewer
- roles/resourcemanager.folderViewer

## Note
The zip file of this source code should be used in the **reporting** terraform feature , to generate reports per customer needs.
 
