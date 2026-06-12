# System Overview

## Core flow

```text
Source data
  -> Spark jobs
  -> Iceberg tables
  -> MinIO object storage
  -> Trino SQL serving
  -> Superset dashboard
```

## Orchestration flow

```text
Airflow DAG
  -> Spark job
  -> Spark quality check
  -> Trino validation SQL
```

## Monitoring flow

```text
Docker containers
  -> cAdvisor
  -> Prometheus
  -> Grafana
```

## Optional AI flow

```text
AI assistant
  -> read-only SQL validator
  -> Trino
  -> Iceberg gold tables
  -> response
```
