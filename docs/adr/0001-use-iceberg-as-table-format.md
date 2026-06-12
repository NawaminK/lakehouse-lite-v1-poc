# ADR 0001: Use Apache Iceberg as the table format

## Status

Accepted for POC.

## Context

The POC needs an open lakehouse table format that can be written by Spark and queried by Trino over S3-compatible storage.

## Decision

Use Apache Iceberg with Parquet data files on MinIO.

## Consequences

- Spark can write Iceberg tables.
- Trino can query the same tables.
- The platform can demonstrate snapshots, schema evolution, metadata tables, and time travel patterns.
- Iceberg maintenance jobs must be added for production-like operation.
