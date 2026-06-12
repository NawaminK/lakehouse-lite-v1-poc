# Lakehouse Core Learning Path

## Goal

Understand how MinIO, Iceberg, Spark, and Trino work together.

## Concepts

- Object storage and S3-compatible paths.
- Iceberg catalog, namespace, table, metadata, snapshot, manifest, data file.
- Spark as write/transform engine.
- Trino as SQL serving engine.

## Hands-on tasks

```bash
make up
make spark-create
docker compose exec trino trino --server http://localhost:8080 --execute "SHOW SCHEMAS FROM iceberg"
docker compose exec trino trino --server http://localhost:8080 --execute "SHOW TABLES FROM iceberg.gold"
docker compose exec trino trino --server http://localhost:8080 --execute "SELECT * FROM iceberg.gold.daily_sales"
```

Inspect Iceberg metadata:

```sql
SELECT * FROM iceberg.gold."daily_sales$snapshots";
SELECT file_path, record_count, file_size_in_bytes FROM iceberg.gold."daily_sales$files";
```

## Key files

- `trino/etc/catalog/iceberg.properties`
- `spark/jobs/01_create_tables.py`
- `spark/jobs/scenarios/*`
- `sql/scenarios/*`
