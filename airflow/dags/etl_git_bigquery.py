import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'trade')
SET_LOCAL_PATH = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

file_name = "wto_indices_prices.csv"
table_name = file_name.replace('.csv', '')
parquet_file_name = file_name.replace('.csv', '.parquet')
dataset_url = f"https://raw.githubusercontent.com/marcsopranzi/sample_data/master/csv/{file_name}"

def read_and_convert_data(src_file):
    data = pv.read_csv(src_file)
    pq.write_table(data, src_file.replace('.csv', '.parquet'))
    
def upload_to_gcs(bucket, object_name, local_file):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="etl_git_bigquery",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['test run'],
) as dag:

    get_data = BashOperator(
        task_id="get_data",
        bash_command=f"curl -sSL {dataset_url} > {SET_LOCAL_PATH}/{file_name}"
    )

    convert_to_parquet = PythonOperator(
        task_id="convert_to_parquet",
        python_callable=read_and_convert_data,
        op_kwargs={
            "src_file": f"{SET_LOCAL_PATH}/{file_name}",
        },
    )

    save_to_storage = PythonOperator(
        task_id="save_to_storage",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{parquet_file_name}",
            "local_file": f"{SET_LOCAL_PATH}/{parquet_file_name}",
        },
    )

    save_to_db = BigQueryCreateExternalTableOperator(
        task_id="save_to_db",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": f"{table_name}",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/{parquet_file_name}"],
            },
        },
    )

    get_data >> convert_to_parquet >> save_to_storage >> save_to_db
