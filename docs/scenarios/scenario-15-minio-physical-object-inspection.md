# Scenario 15: MinIO Physical Object Inspection

Goal: inspect how Iceberg tables appear in object storage.

Manual steps:

1. Open `http://localhost:9001`.
2. Log in with `admin/password`.
3. Open bucket `warehouse`.
4. Inspect table paths such as `gold/daily_sales/` and `scenarios/orders_partitioned/`.

Pass criteria:

- Table paths contain `data/` and `metadata/`.
- Parquet files and Iceberg metadata files are visible.

Learning point:

- Business users should query through Trino/Spark/catalog, not direct object storage paths.

