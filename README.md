# AndreaMonforte-BI-Assignment

This repository contains a compact, production-oriented proof-of-concept data pipeline that ingests daily GA4-style CSV exports from a private Google Cloud Storage bucket, validates and transforms the data, and loads it into BigQuery for analysis. The code is written for deployment as a serverless Cloud Function and can be scheduled to run daily (07:00) via Cloud Scheduler or Workflows.

Repository layout

Root files
- `README.md` — this document.
- `requirements.txt` — Python dependencies used for local testing and deployment.
- `Ingest file specification for GA4.txt` — technical requirements and expected schema for the CSV input.
- `architecture_diagram.png` — architecture diagram illustrating the pipeline components and data flow.
- `small_example_ga4_public_dataset.csv.csv` — small example GA4-style CSV included for local testing and demonstration (placed at repository root).

Top-level folders
- `src/` — source code for the pipeline.
	- `main.py` — Cloud Function entrypoint: lists bucket objects, reports last update, downloads the configured CSV, transforms JSON columns and loads records into BigQuery.
	- `parse_json.py` — CSV parsing helpers and JSON-column unwrapping/transformations used before loading to BigQuery.
	- `config.py` — environment configuration values used by the code. See notes below about demo values.
- `sql/` — example SQL queries and views used for analysis (for example `avg_engagement_time.sql`). These are provided as examples and reference the dataset/table created by the pipeline.
 - `demonstration-screenshots/` — contains two screenshots used for demonstration: one showing the list of BigQuery views, and one showing Cloud Function run logs when the pipeline was executed.

Purpose and scope
- Demonstrates an automated ETL pipeline from GCS to BigQuery using Python and Google Cloud client libraries.
- Focuses on practical deliverables: reproducible code, clear configuration, loading logic, and example analytics queries.

How to use (local test)
1. Provide credentials (service account or ADC):

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

2. Create and activate a virtual environment, then install packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Review `src/config.py` and update values for your environment (project id, bucket name, dataset, table). Note: `src/config.py` in the repository contains demonstration values and should not be used as-is in production.

4. Run a local check (the script will list bucket files and attempt to load the configured CSV):

```bash
python -m src.main
```

What to expect
- The function lists files in the configured bucket and prints the last update time.
- If the target CSV (default `ga4_public_dataset.csv`) is present, it will be downloaded, parsed (JSON columns unwrapped), and loaded into BigQuery.
- The pipeline creates the target dataset automatically if missing.

Deployment notes (Cloud Function + Scheduler)
- Deploy the `src` package as a Cloud Function with an HTTP trigger in the desired region (or Cloud Run). Use the provided service account for correct permissions when deploying to the assignment project.
- Configure Cloud Scheduler to POST to the function URL daily at 07:00 and grant Scheduler the permission to invoke the function.
- For production workloads consider: structured logging, retries, monitoring/alerts, IAM least privilege, and an idempotent ingestion strategy (deduplication, partitioning, append vs truncate).

Validation and file requirements
- See `Ingest file specification for GA4.txt` for the accepted filename (`ga4_public_dataset.csv`), encoding, delimiter, required columns and field formats. Follow these rules to ensure reliable processing.

SQL and analysis
- Example SQL views are located in `sql/` (for example `avg_engagement_time.sql`). These demonstrate how to unpack nested `event_params` and compute session-level metrics such as average engagement time and top-performing page titles.

Files and responsibilities (quick reference)
- `src/main.py` — pipeline orchestration and BigQuery load logic.
- `src/parse_json.py` — CSV to record conversion, JSON unwrapping and minor type coercion.
- `src/config.py` — configuration (DEMO values). Do not commit secrets or real credentials.
- `sql/` — analytical SQL examples and views used to validate and surface insights.
- `Ingest file specification for GA4.txt` — canonical requirements for input files.

Skills and technologies demonstrated
- Languages & libraries: Python, pandas, pyarrow, google-cloud-storage, google-cloud-bigquery
- Cloud & services: Google Cloud Storage, BigQuery, Cloud Functions (or Cloud Run), Cloud Scheduler / Workflows
- Concepts: ETL/ELT, schema validation, JSON unwrapping, BigQuery load jobs, SQL views for analytics, automation and scheduling, idempotent ingestion considerations

Notes and disclaimers
- `src/config.py` contains demonstration values. Variable names in `config.py` do not reference real production datasets except for the GA4-related file name (`ga4_public_dataset.csv`) which maps to publicly documented GA4 exports. Replace values with real project/bucket identifiers before deployment.

Deliverables and presentation
- Code for the ingestion pipeline (`src/`), example SQL queries and views (`sql/`), the ingest specification, and an architecture diagram are included in this repository.