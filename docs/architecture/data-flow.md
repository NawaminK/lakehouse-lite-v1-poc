# Data Flow

## Baseline pipeline

```text
Spark sample data generation
  -> bronze.orders_raw
  -> silver.orders_clean
  -> gold.daily_sales
  -> Trino query
  -> Superset dashboard
```

## CSV ingestion pattern

```text
CSV file
  -> landing area
  -> Spark read CSV
  -> validation and type casting
  -> bronze raw table
  -> silver clean table
  -> gold aggregate table
  -> Trino/Superset
```

## Visual ingestion pattern

```text
NiFi or Hop
  -> MinIO landing zone
  -> Spark Iceberg writer
  -> Trino
  -> Superset
```
