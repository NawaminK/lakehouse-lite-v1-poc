# System Overview

Lakehouse Lite is organized as a local data platform. Each service has one main responsibility, and the learning value comes from watching data move across those responsibilities.

## Core flow

```text
Source data
  -> Spark jobs
  -> Iceberg tables
  -> MinIO object storage
  -> Trino SQL serving
  -> Superset dashboard
```

Plain-language version:

1. Source files provide sample business data.
2. Spark turns those files into structured tables.
3. Iceberg records table metadata, schema, snapshots, and file locations.
4. MinIO stores the physical data and metadata files.
5. Trino lets people query the tables with SQL.
6. Superset uses Trino to build BI charts and dashboards.

Key local docs:

- `docs/learning/plain-language-guide.md`
- `docs/learning/glossary.md`
- `docs/architecture/data-flow.md`
- `docs/architecture/component-responsibility.md`

## Orchestration flow

```text
Airflow DAG
  -> Spark job
  -> Spark quality check
  -> Trino validation SQL
```

Airflow does not store or transform data by itself. It coordinates the order of work: create/update tables, run quality checks, and run SQL validation.

## Monitoring flow

```text
Docker containers
  -> cAdvisor
  -> Prometheus
  -> Grafana
```

Monitoring helps answer operational questions such as:

- Are the containers running?
- Are metrics being collected?
- Is there enough signal to debug a local failure?

## Optional AI flow

```text
AI assistant
  -> read-only SQL validator
  -> Trino
  -> Iceberg gold tables
  -> response
```

The optional AI assistant is intentionally narrow. It validates SQL as read-only and queries curated Iceberg gold tables through Trino.

## Learning Map

| Question | Start here | Then read |
|---|---|---|
| What is this project? | `docs/learning/plain-language-guide.md` | `README.md` |
| What do these terms mean? | `docs/learning/glossary.md` | `docs/references.md` |
| How does data move? | `docs/architecture/data-flow.md` | `docs/learning/lakehouse-learning-path.md` |
| How do I run it? | `README.md` | `docs/runbooks/startup-shutdown.md` |
| How do I test behavior? | `docs/scenarios/index.md` | `docs/poc_test_scenarios.md` |
| How do I troubleshoot? | `docs/runbooks/troubleshooting.md` | `docs/runbooks/service-health-checklist.md` |
