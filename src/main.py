from google.cloud import storage, bigquery
from datetime import datetime
from config import BUCKET_NAME, FILE_NAME, GCP_PROJECT, BQ_DATASET, BQ_TABLE
from parse_json import transform_csv_bytes_to_records


def ensure_dataset_exists():
    bq_client = bigquery.Client()
    dataset_ref = bigquery.DatasetReference(GCP_PROJECT, BQ_DATASET)

    try:
        bq_client.get_dataset(dataset_ref)
        print(f"dataset '{BQ_DATASET}' exists already.")
    except Exception:
        print(f"dataset '{BQ_DATASET}' not found, creating it now...")
        bq_client.create_dataset(bigquery.Dataset(dataset_ref))
        print(f"dataset created.")


def manage_bucket_files():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blobs = list(bucket.list_blobs())

    if blobs == []:
        print("bucket is empty")
        return

    print(f"files found in bucket {BUCKET_NAME}:\n")
    for blob in blobs:
        print(f"{blob.name} - last modified: {blob.updated}\n")
    
    # Find the most recent update timestamp among all blobs
    last_updated = max(blob.updated for blob in blobs)
    print(f"last bucket update: {last_updated.strftime('%Y-%m-%d %H:%M:%S')}\n")


def load_records_to_bigquery(records):
    if not records:
        print("No records to load.")
        return

    bq_client = bigquery.Client()
    table_id = f"{GCP_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"
    table_ref = bigquery.TableReference.from_string(table_id)
    
    # Configure load job to accept newline-delimited JSON
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        max_bad_records=100
    )

    print(f"Loading {len(records)} records into {table_id} ...\n")
    load_job = bq_client.load_table_from_json(
        json_rows=records,
        destination=table_ref,
        job_config=job_config
    )
    load_job.result() # Wait for job to complete
    table = bq_client.get_table(table_ref)
    print(f"Loaded rows: {table.num_rows}")


def load_csv_to_bigquery_transformed():
    ensure_dataset_exists()

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(FILE_NAME)

    if not blob.exists():
        raise FileNotFoundError(f"File {FILE_NAME} not found in bucket {BUCKET_NAME}")

    print(f"Downloading {FILE_NAME} from bucket {BUCKET_NAME} ...")
    csv_bytes = blob.download_as_bytes()
    print(f"Downloaded {len(csv_bytes)} bytes.")

    print("Transforming CSV rows (parsing JSON columns)...")
    # Parse CSV and transform JSON columns
    records = transform_csv_bytes_to_records(csv_bytes)
    print(f"Transformed to {len(records)} records.")

    load_records_to_bigquery(records)


def main(event=None, context=None):
    print("Starting Function")
    manage_bucket_files()
    try:
        load_csv_to_bigquery_transformed()
        return "Load started/completed\n", 200
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}\n", 500


if __name__ == "__main__":
    main()