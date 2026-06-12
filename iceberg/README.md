# Iceberg REST Catalog

The POC uses the Apache Iceberg REST fixture as a lightweight catalog service.

## Purpose

- Keeps Spark and Trino aligned on table definitions.
- Exposes Iceberg catalog operations over REST.
- Points tables to files stored in MinIO.

## Notes

This REST fixture is good for a local POC. Evaluate Apache Polaris or Nessie for a production-like catalog roadmap.
