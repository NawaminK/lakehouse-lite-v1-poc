# Naming Conventions

Consistent names make it easier for Spark, Trino, Airflow, Superset, and teammates to talk about the same object.

## Catalog

Use one Iceberg catalog in this POC:

```text
lakehouse
```

Trino exposes the same catalog as:

```text
iceberg
```

## Namespaces

Use these namespaces:

| Namespace | Purpose |
|---|---|
| `bronze` | Raw or lightly parsed source data |
| `silver` | Cleaned, typed, validated records |
| `gold` | Business-facing aggregates or curated tables |
| `scenarios` | Isolated tutorial/test scenario tables |

## Tables

Use lowercase snake case.

Examples:

```text
lakehouse.bronze.orders_raw
lakehouse.silver.orders_clean
lakehouse.gold.daily_sales
lakehouse.scenarios.customers_current
```

## Columns

Use lowercase snake case and stable business names.

Recommended suffixes:

| Suffix | Meaning |
|---|---|
| `_id` | Identifier |
| `_dt` | Date |
| `_ts` | Timestamp |
| `_at` | Event or processing timestamp |
| `_count` | Count metric |

## Scenario IDs

Scenario files should use two digits:

```text
03_schema_evolution.py
04_cdc_merge_upsert.py
```

Task IDs and docs should keep the same number so logs, docs, and scripts line up.

