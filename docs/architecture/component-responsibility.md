# Component Responsibility

| Component | Responsibility | Not responsible for |
|---|---|---|
| MinIO | Object storage for data and metadata files | Query execution |
| Iceberg REST Catalog | Table catalog and metadata access | Storing data files |
| Spark | Data ingestion, transformation, Iceberg writes | BI dashboards |
| Trino | SQL serving and metadata inspection | Heavy ETL jobs |
| Superset | SQL Lab, datasets, charts, dashboards | Data transformation |
| Airflow | Scheduling and task orchestration | Distributed processing |
| Prometheus | Metrics storage and querying | Business data storage |
| Grafana | Monitoring dashboards | Data pipeline execution |
| cAdvisor | Container metrics exporter | Application tracing |
| AI Assistant | Controlled read-only SQL API for AI | Direct storage access |
