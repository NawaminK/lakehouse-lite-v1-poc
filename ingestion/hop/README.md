# Apache Hop Experiment

Recommended POC pattern:

```text
Hop visual pipeline -> Parquet/CSV landing -> Spark job -> Iceberg table
```

Hop is useful for visual ETL design. For this POC, Spark should remain the component that writes Iceberg tables.
