# AndreaMonforte-BI-Assignment

Project: automated daily CSV ingestion and analysis on GCP

Summary
This repository contains a serverless data ingestion solution that loads a daily CSV file from a private Google Cloud Storage bucket into BigQuery, performs light validation, and prepares the data for analysis. The provided Python script is designed to be used inside a Cloud Function and can be scheduled to run daily at 07:00 via Cloud Scheduler or Workflows.

Key components
- `main.py`: Python script (Cloud Function entrypoint) that lists bucket objects, reports last update time, ensures the BigQuery dataset exists, and loads the specified CSV into BigQuery.
- `config.py`: configuration values (bucket name, file name, GCP project, dataset, table, function URL).
- `requirements.txt`: dependencies required for local testing and deployment (`google-cloud-storage`, `google-cloud-bigquery`).
- `Ingest file specification for GA4.txt`: technical requirements and schema expectations for incoming CSV files.
- `.gcloudignore`: files excluded from Cloud deployments.

Principles and behaviour
- The function targets a single file name: `ga4_public_dataset.csv` in bucket `platform_assignment_bucket` (region `europe_west4`).
- Dataset is created if missing. The CSV load uses BigQuery's CSV loader with header skip and autodetection. The table write disposition is currently configured to overwrite (`WRITE_TRUNCATE`).
- The ingest specification documents required columns, formats and encoding rules—follow it to ensure reliable processing.

Quick start (local test)
1. Authenticate to GCP (use a service account with required permissions):

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Review or update `config.py` to match your environment.

4. Run the script locally for a quick check (it will use Application Default Credentials):

```bash
python main.py
```

Deployment notes (Cloud Function + Scheduler)
- Deploy the function with an HTTP trigger (or Cloud Functions second gen with Cloud Run): set region `europe-west4` and run as the provided service account.
- Use Cloud Scheduler to POST to the function URL daily at 07:00. Ensure the Scheduler has permission to invoke the function.
- Consider switching BigQuery write disposition to `WRITE_APPEND` and adding deduplication if you want incremental loads instead of overwrite.

SQL views and analysis
- Create BigQuery views for descriptive analytics and nested-field exploration. Example analyses include top-performing page titles by total page views and other marketing KPIs. Store views in the `andrea_monforte_dataset` dataset.

Files of interest
- `main.py` — ingestion and bucket listing logic.
- `config.py` — project configuration (do not commit secrets; a `.gitignore` entry for `config.py` is present in the repository).
- `Ingest file specification for GA4.txt` — validation rules and expected schema for incoming files.
- Architecture diagram — included in the repository attachments; use it when preparing your presentation.

License
This repository is delivered as part of the assignment. No external license is declared.

