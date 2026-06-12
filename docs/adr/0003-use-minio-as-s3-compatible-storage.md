# ADR 0003: Use MinIO as S3-compatible storage

## Status

Accepted for POC.

## Context

The POC runs on-prem on a single Ubuntu host and needs an S3-compatible object storage service.

## Decision

Use MinIO as the local S3-compatible storage layer.

## Consequences

- The POC can run without cloud dependency.
- Spark, Trino, and Iceberg REST Catalog must use the same endpoint and credentials.
- Standalone MinIO is acceptable for POC but not a production architecture.
