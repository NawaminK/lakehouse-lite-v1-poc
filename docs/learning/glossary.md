# Glossary

Use this glossary when a lakehouse or platform term appears in the project. Each entry explains the idea in plain language and points to local docs plus external references.

| Term | Plain meaning | Where it appears here | Learn more |
|---|---|---|---|
| Lakehouse | A data platform pattern that combines data lake storage with warehouse-style tables and SQL access | `README.md`, `docs/architecture/system-overview.md` | `docs/references.md#lakehouse-core` |
| POC | Proof of concept; a small version built to learn and validate decisions | `README.md`, `docs/security/poc-vs-production.md` | `docs/references.md#beginner-orientation` |
| Docker Compose | A way to start many local containers from one file | `docker-compose.yml`, `Makefile` | `docs/references.md#local-platform-and-github-workflow` |
| Object storage | File storage organized as buckets and objects instead of local folders | `minio`, `warehouse`, `data/`, `metadata/` | `docs/references.md#lakehouse-core` |
| S3-compatible storage | Storage that behaves like Amazon S3 APIs; MinIO provides this locally | `docker-compose.yml`, `trino/etc/catalog/iceberg.properties` | `docs/references.md#lakehouse-core` |
| MinIO | The local object storage service used by this POC | `http://localhost:9001` | `docs/references.md#lakehouse-core` |
| Apache Iceberg | A table format that tracks data files, schemas, snapshots, and metadata for lakehouse tables | `spark/jobs/`, `sql/scenarios/`, Trino metadata queries | `docs/references.md#lakehouse-core` |
| Catalog | A service or configuration that lets tools find Iceberg tables and metadata | Iceberg REST Catalog service on `http://localhost:8181` | `docs/references.md#lakehouse-core` |
| Namespace | A grouping for tables, similar to a database schema | `bronze`, `silver`, `gold` | `docs/architecture/naming-conventions.md` |
| Snapshot | A recorded version of an Iceberg table after a change | Scenario 5, metadata inspection queries | `docs/scenarios/scenario-05-time-travel-snapshots.md` |
| Time travel | Querying an older table snapshot | Scenario 5 | `docs/scenarios/scenario-05-time-travel-snapshots.md` |
| Schema evolution | Changing a table schema safely over time | Scenario 3 | `docs/scenarios/scenario-03-schema-evolution.md` |
| Partitioning | Organizing table files by values such as date to improve maintenance and query planning | Scenario 6 | `docs/scenarios/scenario-06-partition-file-layout.md` |
| Spark | The engine that reads, transforms, and writes data | `spark/jobs/01_create_tables.py` | `docs/references.md#data-engineering` |
| Trino | The SQL engine used to query Iceberg tables | `sql/`, `trino/etc/catalog/` | `docs/references.md#lakehouse-core` |
| Superset | The BI tool used for dashboard exploration | `superset/`, `http://localhost:8088` | `docs/references.md#bi-and-dashboarding` |
| Airflow | The workflow scheduler that runs jobs in order | `airflow/dags/` | `docs/references.md#orchestration` |
| DAG | Directed acyclic graph; an Airflow workflow made of ordered tasks | `airflow/dags/lakehouse_v1_poc.py` | `docs/learning/airflow-learning-path.md` |
| Bronze | The raw or lightly processed layer | `iceberg.bronze.orders_raw` | `docs/architecture/data-flow.md` |
| Silver | The cleaned and standardized layer | `iceberg.silver.orders_clean` | `docs/architecture/data-flow.md` |
| Gold | The business-ready reporting layer | `iceberg.gold.daily_sales` | `docs/architecture/data-flow.md` |
| Data quality | Checks that confirm data is valid, complete, or within expected rules | `spark/jobs/02_quality_checks.py`, scenario 7 | `docs/scenarios/scenario-07-quality-failure-expected.md` |
| SQL assertion | A SQL check that fails when an expected condition is not true | `sql/scenarios/03_scenario_assertions.sql` | `docs/scenarios/scenario-12-trino-sql-assertions.md` |
| CDC | Change data capture; applying inserts, updates, and deletes from a source system | Scenario 4 | `docs/scenarios/scenario-04-cdc-merge-upsert.md` |
| Upsert | Update existing rows and insert new rows in one operation | Scenario 4 | `docs/scenarios/scenario-04-cdc-merge-upsert.md` |
| Backfill | Loading or correcting data for a past date or period | Scenario 9 | `docs/scenarios/scenario-09-late-arriving-backfill.md` |
| Observability | The ability to understand system health from metrics, logs, and checks | `prometheus/`, `monitoring/`, scenario 16 | `docs/references.md#observability` |
| Prometheus | Metrics collection system | `http://localhost:9090` | `docs/references.md#observability` |
| Grafana | Dashboard tool for metrics | `http://localhost:3000` | `docs/references.md#observability` |
| cAdvisor | Container metrics exporter used by Prometheus | `http://localhost:8090` | `docs/references.md#observability` |
| Runbook | A practical troubleshooting or operating guide | `docs/runbooks/` | `docs/runbooks/troubleshooting.md` |
| Scenario | A repeatable exercise that proves one platform behavior | `scenarios.json`, `docs/scenarios/` | `docs/scenarios/index.md` |
| Definition of Done | A checklist for whether a change is ready to merge | `docs/engineering/definition-of-done.md` | `docs/github-workflow.md` |
| Read-only query API | A safe API layer that allows SELECT-style SQL without table changes | `ai-assistant/` | `docs/learning/ai-learning-path.md` |
