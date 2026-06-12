# Spark and Data Engineering Learning Path

## Goal

Build repeatable ingestion and transformation jobs that write Iceberg tables.

## Concepts

- SparkSession.
- DataFrame read/write.
- CSV and Parquet ingestion.
- Data type casting.
- Bronze, silver, and gold layers.
- Data quality checks and rejected records.
- Iceberg writes with `writeTo(...).using("iceberg")`.

## Hands-on tasks

1. Read a CSV file with Spark.
2. Cast columns to expected types.
3. Write a bronze Iceberg table.
4. Filter invalid records into a rejected table.
5. Aggregate a gold table.
6. Query the gold table with Trino.

## Key files

- `spark/jobs/01_create_tables.py`
- `spark/jobs/02_quality_check.py`
- `spark/jobs/scenarios/`
- `sample-data/csv/`
