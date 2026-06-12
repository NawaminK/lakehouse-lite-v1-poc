# Spark Jobs

Spark is the main processing engine for this POC.

## Responsibilities

- Read source files or landing data.
- Clean and validate data.
- Write Iceberg bronze, silver, and gold tables.
- Run scenario tests such as schema evolution, CDC, time travel, and backfill.

## Baseline commands

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/01_create_tables.py
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/02_quality_check.py
```

## Add a new ingestion job

Start from:

```text
spark/jobs/templates/csv_to_bronze_silver_gold.py
```

The baseline job reads `sample-data/csv/orders.csv`, which is mounted into the Spark container at:

```text
/home/iceberg/sample-data/csv/orders.csv
```
