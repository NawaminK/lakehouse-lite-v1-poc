# Architecture

```text
Source/sample data
  -> Spark job
  -> Iceberg bronze/silver/gold tables
  -> MinIO bucket: s3://warehouse
  -> Iceberg REST Catalog metadata
  -> Trino SQL
  -> Superset BI
  -> Airflow orchestration
  -> Prometheus/Grafana/cAdvisor monitoring
```

## POC decisions

- Storage: MinIO standalone mode.
- Table format: Apache Iceberg with Parquet data files.
- Catalog: Apache Iceberg REST fixture for a lightweight POC.
- ETL engine: Spark.
- SQL engine: Trino.
- BI: Superset.
- Orchestration: Airflow standalone.
- Monitoring: Prometheus + Grafana + cAdvisor.

## Not production-ready

This POC intentionally skips HA, TLS, SSO, Ranger/OPA policy, secrets management, backup, object-locking, distributed MinIO, and production Airflow metadata DB.
