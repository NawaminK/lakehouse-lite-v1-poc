# Scenario 10: Trino Catalog Discovery

Goal: confirm Trino can discover Iceberg schemas, tables, and columns created by Spark.

Run:

```bash
docker compose exec trino trino --server http://localhost:8080 --file /tmp/sql/scenarios/01_catalog_discovery.sql
```

Pass criteria:

- Trino sees the `iceberg` catalog.
- Trino sees `bronze`, `silver`, `gold`, and `scenarios` schemas.
- Trino can list columns for `gold.daily_sales` and scenario tables.

