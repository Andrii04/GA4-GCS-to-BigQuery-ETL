# AndreaMonforte-BI-Assignment

Purpose
This repository contains the implementation and supporting assets for an automated daily CSV ingestion pipeline to BigQuery. It is prepared as an assignment deliverable and documents how to run, deploy and verify the solution.

Repository contents
- `main.py` — Cloud Function entrypoint: lists bucket files, reports last update, ensures the BigQuery dataset, and loads the CSV into BigQuery.
- `config.py` — environment-specific values (bucket, file name, project, dataset, table, function URL).
- `requirements.txt` — Python dependencies for local testing and deployment.
- `Ingest file specification for GA4.txt` — technical requirements and expected schema for the input CSV.
- `.gcloudignore` — files excluded from Cloud deployments.
- `Architecture_Diagram.drawio.png`— flowchart of the project.

Prerequisites
- A GCP project with the necessary IAM roles. The provided project id is `crystalloids-candidates`.
- Python 3.8+ and `pip`.
- A service account key or Application Default Credentials with permissions for Storage and BigQuery.

Usage — local test
1. Configure credentials (use a service account key):

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Confirm `config.py` values match your environment. Do not commit secret keys.

4. Run the script to perform a local check (it will access the configured bucket and attempt to load the configured file):

```bash
python main.py
```

Expected result: the script prints the list of files in the bucket, last update time, and attempts to load `ga4_public_dataset.csv` into BigQuery. The script creates the dataset if it does not exist and uses BigQuery's CSV loader.

Deployment (Cloud Function + Scheduler)
1. Deploy the function with an HTTP trigger in `europe-west4`. Use the assignment service account when deploying for correct permissions.

2. Configure Cloud Scheduler to send an HTTP POST to the function URL daily at 07:00. Ensure Scheduler has invoke permissions.

Example considerations
- Current behavior: the load job uses `WRITE_TRUNCATE` (overwrites the target table). For production, consider `WRITE_APPEND` with deduplication or an incremental ingestion strategy.
- Add structured logging, retries, monitoring and alerts for production readiness.

Validation and analysis
- The file ingest specification (`Ingest file specification for GA4.txt`) documents required headers, types and encoding. Follow it to ensure reliable ingestion.
- Create BigQuery views for analysis (e.g., top page titles by pageviews). Store these views under the configured dataset.

Deliverables
- This repository (Python ingestion script and assets).
- Deployed Cloud Function and scheduled workflow (if deployed to GCP).
- BigQuery views and any SQL used for analysis.

Notes and assumptions
- The repository is intended for assignment use by a single contributor. `config.py` is included for convenience but should be ignored in shared repos if it contains secrets.