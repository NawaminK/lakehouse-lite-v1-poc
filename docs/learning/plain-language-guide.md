# Plain-Language Guide

This guide is for readers who are new to lakehouse, data engineering, or the tools used in this repository.

## One-Sentence Version

Lakehouse Lite is a small local data platform that shows how raw business data becomes trusted tables, SQL queries, dashboards, scheduled jobs, and monitoring signals.

## Why This Project Exists

Most data teams need to answer a few practical questions:

- Where does the data live?
- How do we clean and organize it?
- How do analysts query it?
- How do we know the pipeline is healthy?
- How can a team learn and improve the platform safely?

This POC answers those questions on one machine with Docker Compose. It is intentionally small enough to learn from, but it uses tools and patterns that resemble a real lakehouse platform.

## The Story Of One Order

Follow one order through the system:

1. The source file starts in `sample-data/csv/orders.csv`.
2. Spark reads the CSV and writes a raw table called `bronze.orders_raw`.
3. Spark cleans and standardizes the data into `silver.orders_clean`.
4. Spark aggregates business metrics into `gold.daily_sales`.
5. Iceberg tracks table metadata, snapshots, schema changes, and data files.
6. MinIO stores the physical files and Iceberg metadata.
7. Trino queries the Iceberg tables with SQL.
8. Superset can build dashboards from the Trino tables.
9. Airflow can run the jobs in the right order.
10. Prometheus, Grafana, and cAdvisor help the team see whether containers and services are healthy.

The important idea: each tool has a focused job, and the project demonstrates how those jobs connect.

## What Each Component Does

| Component | Plain meaning | In this project |
|---|---|---|
| Docker Compose | Starts all local services together | Runs the POC stack from `docker-compose.yml` |
| MinIO | Local S3-compatible file storage | Stores Iceberg data and metadata files |
| Apache Iceberg | Table format for data lake tables | Tracks snapshots, schema evolution, partitions, and files |
| Spark | Data transformation engine | Creates and updates bronze, silver, and gold tables |
| Trino | SQL query engine | Lets users query Iceberg tables with SQL |
| Superset | BI and dashboard tool | Connects to Trino and visualizes gold tables |
| Airflow | Workflow scheduler | Runs Spark jobs and validation steps |
| Prometheus | Metrics collector | Scrapes container and platform metrics |
| Grafana | Metrics dashboard tool | Displays Prometheus metrics |
| cAdvisor | Container metrics exporter | Exposes container CPU, memory, and runtime metrics |
| AI Assistant | Optional query API | Allows read-only SQL access to curated tables |

## Core Ideas In Plain Language

### Bronze, Silver, Gold

These are table layers:

- Bronze keeps data close to the source.
- Silver cleans and standardizes data.
- Gold prepares data for reporting or business use.

### Iceberg Snapshots

An Iceberg table keeps a history of changes. A snapshot is like a recorded version of the table at a point in time. This makes time travel, rollback, and metadata inspection possible.

### SQL Serving

Spark is good at transforming data. Trino is good at interactive SQL queries. This project uses Spark to write tables and Trino to serve them to users and BI tools.

### Quality Gates

A quality gate is a check that stops bad data from being accepted. In this POC, quality checks and SQL assertions help prove that the output table is trustworthy.

### Scenarios

Scenarios are guided tests of important lakehouse behaviors, such as schema evolution, CDC upsert, time travel, late-arriving data, metadata inspection, and recovery.

## First Things To Try

Start the platform:

```bash
cp .env.example .env
make up
make smoke
```

Create the baseline tables:

```bash
make spark-create
make spark-quality
```

Query the business output:

```bash
docker compose exec trino trino --server http://localhost:8080 --catalog iceberg --schema gold --execute "SELECT * FROM daily_sales ORDER BY order_dt, province"
```

Then read:

- `docs/learning/glossary.md` for key terms.
- `docs/architecture/system-overview.md` for the system map.
- `docs/scenarios/index.md` for guided scenario learning.
- `docs/references.md` for official documentation by topic.

## What To Learn Next

If you are brand new, follow this order:

1. Read this guide.
2. Read `docs/learning/glossary.md`.
3. Run the quick start in `README.md`.
4. Follow `docs/learning/onboarding-journey.md`.
5. Pick one focused learning path in `docs/learning/`.
6. Use `docs/references.md` when a term or tool needs deeper study.
