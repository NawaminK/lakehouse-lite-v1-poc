# Spark Job Templates

Use these files when adding a new ingestion pattern. Copy a template, rename it, and keep the same structure unless the source requires something different.

## Templates

| Template | Purpose |
|---|---|
| `csv_to_bronze_silver_gold.py` | CSV source to bronze, silver, rejected records, and gold aggregate |

## Recommended workflow

1. Read from a source or landing path.
2. Write source-shaped data to bronze.
3. Cast and validate into silver.
4. Write rejected records when rows fail validation.
5. Build a gold table for business-facing queries.
6. Add a Trino assertion query.
7. Add an Airflow task only after the Spark job works by itself.

