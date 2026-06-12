# Ingestion UX

This folder is reserved for visual ingestion experiments.

Recommended patterns:

```text
NiFi -> MinIO landing zone -> Spark -> Iceberg
Hop -> Parquet landing files -> Spark -> Iceberg
```

Do not make NiFi or Hop responsible for the full Lakehouse transformation flow in the first phase. Keep Spark responsible for Iceberg writes.
