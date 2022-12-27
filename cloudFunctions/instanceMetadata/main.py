import os
from google.auth import compute_engine
from google.cloud import storage
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from project_discovery import ProjectDiscovery
from instance_collector import InstanceCollector
from datetime import datetime

credentials = compute_engine.Credentials()

def upload_to_bucket(blob_name, bucket_name, content, contenttype):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(content, content_type=contenttype, client=None, predefined_acl=None)
    return blob

def get_schema():
    schema = [
        bigquery.SchemaField("PROJECT", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("ID", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("NAME", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("ZONE", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("STATUS", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("GENDATE", "DATETIME", mode="REQUIRED"),
    ]
    return schema

def table_exists(bq_client, table_id):
    print("--------CHECKING TABLE EXISTS .... -----------------")
    table_exists = 'false'
    try:
        bq_client.get_table(table_id)  # Make an API request.
        print("Table {} already exists.".format(table_id))
        table_exists = 'true'
    except NotFound:
        print("Table {} is not found.".format(table_id))

    return table_exists


def create_table(bq_client,table_id,schema_definition):
    print("-------------CREATING TABLE---------------")
    table = bigquery.Table(table_id, schema=schema_definition)
    table = bq_client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )
    return table.table_id

def clear_table_data(bigquery_client, dataset_id, table_name):
    bq_retention = os.getenv("BQ_RETENTION", 13)
    query = f'DELETE `{dataset_id}.{table_name}` WHERE DATETIME_DIFF( CURRENT_DATETIME("UTC"), gendate, MONTH) > {bq_retention}'

    query_job = bigquery_client.query(query)
    query_job.result()
    print(f"Clear data in {dataset_id} for retention {bq_retention} - done.")

def load_data_to_bq(bigquery_client, dataset_id, table_name, bucket_name, json_path, schema_definition):
    dataset_ref = bigquery_client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.schema = schema_definition
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    uri = "gs://"+bucket_name+"/"+json_path

    dataset = bigquery_client.get_dataset(dataset_id)

    clear_table_data(bigquery_client, dataset_id, table_name)
    load_job = bigquery_client.load_table_from_uri(
        uri,
        dataset_ref.table(table_name),
        location=dataset.location,
        job_config=job_config,
    )  

    print("Starting job {}".format(load_job.job_id))

    load_job.result() 
    print("Job finished.")

    destination_table = bigquery_client.get_table(dataset_ref.table(table_name))
    print("Loaded {} rows.".format(destination_table.num_rows))


def main(request):
    try:
        data = ""
        curr_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        show_deleted = False
        project_discovery = ProjectDiscovery(show_deleted)
        instance_collector = InstanceCollector()

        
        parents = os.environ.get('PARENT_FOLDERS').split(",")
        projects_list = []
        for parent in parents:
            projects_list.extend(project_discovery.lister("folders/"+parent.strip()))

        
        for project_obj in projects_list:
            project_id = project_obj.get("projectId")
            print("Project {} .".format(project_id))
            try:
                instance_list = instance_collector.getObjectsListPage(project_id, None)
            except Exception as e:
                print("exception {} for project {}".format(e, project_id))
                instance_list = ""

            for zone in instance_list:
                zone_data = instance_list.get(zone)
                if "instances" in zone_data:
                    for instance in zone_data["instances"]:
                        tmp={}
                        tmp['project'] = project_id
                        tmp['id'] = instance['id']
                        tmp['name'] = instance['name']
                        tmp['zone'] = zone[6:]
                        tmp['status'] = instance['status']
                        tmp['gendate'] = curr_date
                        
                        tmp = str(tmp).replace("'", '"')
                        data += tmp + '\n'

        print("---------------------------DATA-------------------------------")    
        print(data)
        
        bucket_name = os.environ.get('BUCKET_NAME')
        filename = "metadata.json"
        json_path = "json/" + filename

        #Upload file to cloud storage 
        upload_to_bucket(json_path, bucket_name, data, 'application/json')
        
        bq_client = bigquery.Client()
        table_name = os.environ.get("TABLE_NAME")
        dataset_id = os.environ.get("DATASET_ID")
        bq_project = os.environ.get("BQ_PROJECT")
        table_id = bq_project + "." + dataset_id + "." + table_name #bq_project.dataset_id.table_name project id can be changed

        is_table = table_exists(bq_client, table_id) #Check table exists or not
        
        schema_definition = get_schema() #Get schema definition

        if is_table == 'false':
            create_table(bq_client, table_id, schema_definition) #Creating table
        
        #Load data using json file
        load_data_to_bq(bq_client, dataset_id, table_name, bucket_name, json_path, schema_definition)

    except Exception as e:
        print("---------EXCEPTION OCCURRED---------", e)
