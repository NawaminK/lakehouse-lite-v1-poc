# MinIO

MinIO is the S3-compatible object storage layer for this POC.

## Purpose

- Stores Iceberg metadata files.
- Stores Parquet data files.
- Stores landing data for future ingestion workflows.

## Console

- URL: http://localhost:9001
- Username: admin
- Password: password

## Buckets

- `warehouse`: Iceberg warehouse and landing area.
- `raw`: optional raw landing bucket for experiments.
