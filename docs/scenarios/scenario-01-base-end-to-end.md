# Scenario 01: Base End-to-End Lakehouse Path

Goal: prove the minimum working path from Spark writes to Trino reads.

Run:

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/01_create_tables.py
```

What it creates:

- `lakehouse.bronze.orders_raw`
- `lakehouse.silver.orders_clean`
- `lakehouse.gold.daily_sales`

Pass criteria:

- Spark exits successfully.
- Bronze, silver, and gold tables exist.
- Trino can query `iceberg.gold.daily_sales`.

