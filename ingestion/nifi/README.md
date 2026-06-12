# NiFi Experiment

Recommended POC pattern:

```text
GetFile / InvokeHTTP / QueryDatabaseTable -> PutS3Object -> MinIO landing -> Spark -> Iceberg
```

NiFi is useful for drag-and-drop ingestion, routing, retries, and provenance.
