# Lakehouse Lite v1 POC

Lakehouse Lite is a single-node, open-source lakehouse proof of concept for Ubuntu 24.04 and Docker Compose. It is designed for learning how a modern data platform works end to end: local storage, table metadata, data engineering jobs, SQL serving, dashboards, orchestration, monitoring, and optional AI-assisted querying.

This repository is also organized as a team learning project. New teammates can start from the plain-language docs, choose a team track, run the local stack, and make small pull requests with clear validation evidence.

## Table Of Contents

- [What This Project Does](#what-this-project-does)
- [Architecture At A Glance](#architecture-at-a-glance)
- [Core Capabilities](#core-capabilities)
- [Requirements And Planning](#requirements-and-planning)
- [Start Here](#start-here)
- [Quick Start](#quick-start)
- [Service URLs](#service-urls)
- [Common Workflows](#common-workflows)
- [Team Learning Tracks](#team-learning-tracks)
- [Repository Structure](#repository-structure)
- [Documentation Map](#documentation-map)
- [Cleanup](#cleanup)

## What This Project Does

This POC shows how raw business data becomes trusted analytics output:

1. Source files land in the repository as sample data.
2. Spark reads and transforms the data into bronze, silver, and gold tables.
3. Apache Iceberg tracks table metadata, schema changes, snapshots, and physical files.
4. MinIO stores Iceberg data and metadata through an S3-compatible interface.
5. Trino queries Iceberg tables with SQL.
6. Superset connects to Trino for BI exploration and dashboards.
7. Airflow orchestrates jobs and validation steps.
8. Prometheus, Grafana, and cAdvisor expose local platform health signals.
9. The optional AI Assistant exposes a guarded, read-only SQL query API.

Use this project when you want to learn or demonstrate:

- Lakehouse architecture on one machine.
- Spark -> Iceberg -> Trino data flow.
- Bronze/silver/gold data engineering patterns.
- SQL assertions and scenario-based validation.
- Airflow orchestration and Superset dashboard setup.
- Basic observability with Prometheus and Grafana.
- Safe read-only query access for AI experiments.
- Team-based development with GitHub issues, PRs, CODEOWNERS, and CI checks.

## Architecture At A Glance

```text
Source data
  -> Spark jobs
  -> Apache Iceberg tables
  -> MinIO S3-compatible storage
  -> Trino SQL serving
  -> Superset dashboards
  -> Airflow orchestration
  -> Prometheus/Grafana/cAdvisor monitoring
  -> Optional AI Assistant read-only query API
```

<img width="1536" height="1024" alt="Lakehouse Lite architecture" src="https://github.com/user-attachments/assets/a13209ca-ed0d-40dd-bc52-45ac34d32fee" />

Read more:

- [System overview](docs/architecture/system-overview.md)
- [Data flow](docs/architecture/data-flow.md)
- [Component responsibility](docs/architecture/component-responsibility.md)
- [Naming conventions](docs/architecture/naming-conventions.md)
- [Plain-language guide](docs/learning/plain-language-guide.md)

## Core Capabilities

| Area | What it proves | Start here |
|---|---|---|
| Local platform | Docker Compose can run the full POC stack locally | [Startup and shutdown runbook](docs/runbooks/startup-shutdown.md) |
| Lakehouse storage | MinIO + Iceberg can store table data and metadata | [Lakehouse learning path](docs/learning/lakehouse-learning-path.md) |
| Data engineering | Spark can build bronze, silver, and gold tables | [Spark data engineering path](docs/learning/spark-data-engineering-learning-path.md) |
| SQL serving | Trino can query Iceberg tables and metadata | [Trino validation SQL](sql/trino_validation.sql) |
| Data quality | Spark checks and SQL assertions can catch bad outputs | [Scenario assertions](docs/scenarios/scenario-12-trino-sql-assertions.md) |
| Orchestration | Airflow can run jobs and validation in sequence | [Airflow learning path](docs/learning/airflow-learning-path.md) |
| BI | Superset can connect to Trino and inspect gold tables | [Superset connection runbook](docs/runbooks/superset-trino-connection.md) |
| Observability | Prometheus, Grafana, and cAdvisor expose platform signals | [Observability learning path](docs/learning/observability-learning-path.md) |
| AI query API | A small API can enforce read-only SQL access through Trino | [AI Assistant README](ai-assistant/README.md) |
| Team learning | Four teams can learn and improve the platform safely | [Team getting started](docs/team-getting-started.md) |

## Requirements And Planning

Use [Project requirements](docs/requirements.md) as the source of truth for scope, functional requirements, non-functional requirements, validation gates, and traceability to team issues.

Planning links:

- [Project requirements](docs/requirements.md)
- [Team getting started](docs/team-getting-started.md)
- [Team roadmap](docs/team-roadmap.md)
- [Starter backlog](docs/backlog/README.md)
- [GitHub Project Board](https://github.com/users/NawaminK/projects/3)
- [Definition of Done](docs/engineering/definition-of-done.md)

## Start Here

If you are new to lakehouse or data platform work:

1. Read [Plain-language guide](docs/learning/plain-language-guide.md).
2. Use the [Glossary](docs/learning/glossary.md) when a term is unfamiliar.
3. Follow the [Documentation index](docs/README.md).
4. Review the [System overview](docs/architecture/system-overview.md).
5. Review [Project requirements](docs/requirements.md).
6. Choose a team path from [Team getting started](docs/team-getting-started.md).
7. Use [References](docs/references.md) for official docs by topic.

If you want to run the POC immediately:

1. Follow [Quick Start](#quick-start).
2. Run [Baseline validation](#baseline-validation).
3. Try [Extended POC scenarios](#extended-poc-scenarios).
4. Use [Troubleshooting](docs/runbooks/troubleshooting.md) if a service fails.

## Quick Start

```bash
cp .env.example .env
make up
make ps
make smoke
```

Equivalent raw command:

```bash
export AIRFLOW_UID=$(id -u)
export DOCKER_GID=$(stat -c '%g' /var/run/docker.sock 2>/dev/null || stat -f '%g' /var/run/docker.sock 2>/dev/null || echo 999)
docker compose up -d --build
```

Common commands:

```bash
make help
make up
make down
make ps
make logs
make smoke
make scenarios
make validate
make reset
```

## Service URLs

| Service | URL | Default credential | Related docs |
|---|---|---|---|
| MinIO API | http://localhost:9000 | none | [Lakehouse learning path](docs/learning/lakehouse-learning-path.md) |
| MinIO Console | http://localhost:9001 | admin / password | [MinIO inspection scenario](docs/scenarios/scenario-15-minio-physical-object-inspection.md) |
| Iceberg REST Catalog | http://localhost:8181 | none | [Component responsibility](docs/architecture/component-responsibility.md) |
| Spark/Jupyter | http://localhost:8888 | check logs if token is required | [Spark learning path](docs/learning/spark-data-engineering-learning-path.md) |
| Trino | http://localhost:8080 | none | [Lakehouse learning path](docs/learning/lakehouse-learning-path.md) |
| Superset | http://localhost:8088 | admin / admin | [Superset runbook](docs/runbooks/superset-trino-connection.md) |
| Airflow | http://localhost:8081 | admin / admin | [Airflow learning path](docs/learning/airflow-learning-path.md) |
| Prometheus | http://localhost:9090 | none | [Observability learning path](docs/learning/observability-learning-path.md) |
| Grafana | http://localhost:3000 | admin / admin | [Observability smoke test](docs/scenarios/scenario-16-observability-smoke-test.md) |
| cAdvisor | http://localhost:8090 | none | [Service health checklist](docs/runbooks/service-health-checklist.md) |
| AI Assistant, optional | http://localhost:8010 | none | [AI Assistant README](ai-assistant/README.md) |

## Common Workflows

### Baseline Validation

Create tables, run quality checks, and query the business output:

```bash
make spark-create
make spark-quality
docker compose exec trino trino --server http://localhost:8080 --catalog iceberg --schema gold --execute "SELECT * FROM daily_sales ORDER BY order_dt, province"
```

Related docs:

- [Data flow](docs/architecture/data-flow.md)
- [Lakehouse learning path](docs/learning/lakehouse-learning-path.md)
- [Spark data engineering path](docs/learning/spark-data-engineering-learning-path.md)

### Superset

Use this connection URI:

```text
trino://admin@trino:8080/iceberg
```

Then select schema `gold` and table `daily_sales`.

Related docs:

- [Superset-Trino connection runbook](docs/runbooks/superset-trino-connection.md)
- [Superset learning path](docs/learning/superset-learning-path.md)
- [Superset dashboard validation scenario](docs/scenarios/scenario-14-superset-dashboard-validation.md)

### Airflow

Open http://localhost:8081 and trigger:

- `lakehouse_v1_poc`
- `lakehouse_v1_poc_scenarios`

This POC uses Docker socket access from Airflow. This is convenient for local POC work but is not a production security pattern. See [POC vs production security](docs/security/poc-vs-production.md).

Related docs:

- [Airflow learning path](docs/learning/airflow-learning-path.md)
- [Airflow DAG standards](docs/engineering/airflow-dag-standards.md)
- [Startup and shutdown runbook](docs/runbooks/startup-shutdown.md)

### Extended POC Scenarios

Run all scenarios:

```bash
make scenarios
```

Scenario coverage includes platform health, base pipeline, data quality, schema evolution, CDC upsert, time travel, partition/file layout, expected failure, Iceberg maintenance, late-arriving backfill, Trino assertions, metadata inspection, Superset validation, MinIO inspection, observability, and recovery drill.

Related docs:

- [Scenario index](docs/scenarios/index.md)
- [POC test scenarios](docs/poc_test_scenarios.md)
- [Trino SQL assertions](docs/scenarios/scenario-12-trino-sql-assertions.md)

### Optional AI Query API

Start the AI Assistant profile:

```bash
docker compose --profile ai up -d --build ai-assistant
```

Query through Trino safely:

```bash
curl -X POST http://localhost:8010/query \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT province, SUM(net_sales) AS total_net_sales FROM daily_sales GROUP BY province ORDER BY total_net_sales DESC"}'
```

Related docs:

- [AI Assistant README](ai-assistant/README.md)
- [AI learning path](docs/learning/ai-learning-path.md)
- [POC vs production security](docs/security/poc-vs-production.md)

## Team Learning Tracks

| Team | Focus | Getting started |
|---|---|---|
| Team A: Platform + Observability | Docker Compose, Makefile, readiness checks, Prometheus, Grafana, cAdvisor | [Team A guide](docs/team-getting-started.md#team-a-platform--observability) |
| Team B: Lakehouse Core + Data Engineering | MinIO, Iceberg, Spark, Trino, bronze/silver/gold, quality checks | [Team B guide](docs/team-getting-started.md#team-b-lakehouse-core--data-engineering) |
| Team C: Orchestration + BI | Airflow, backfills, Superset datasets, dashboards | [Team C guide](docs/team-getting-started.md#team-c-orchestration--bi) |
| Team D: AI + Ingestion UX | Read-only query API, SQL guardrails, NiFi/Hop experiments | [Team D guide](docs/team-getting-started.md#team-d-ai--ingestion-ux) |

Team docs:

- [Team getting started](docs/team-getting-started.md)
- [Team roadmap](docs/team-roadmap.md)
- [Starter backlog](docs/backlog/README.md)
- [GitHub workflow](docs/github-workflow.md)
- [Definition of Done](docs/engineering/definition-of-done.md)

## Repository Structure

| Path | Purpose |
|---|---|
| `.github/` | GitHub workflow, templates, CODEOWNERS |
| `infra/scripts/` | POC automation and readiness scripts |
| `docs/` | Architecture, runbooks, learning paths, roadmap, references |
| `spark/jobs/` | Spark ETL jobs and scenario jobs |
| `trino/etc/` | Trino configuration and Iceberg catalog config |
| `sql/` | Trino validation and scenario SQL |
| `airflow/dags/` | Airflow DAGs |
| `superset/` | Superset image and BI setup notes |
| `prometheus/` | Prometheus configuration |
| `monitoring/` | Monitoring docs and future dashboards |
| `ai-assistant/` | Optional read-only Trino query API |
| `ingestion/` | Optional NiFi/Hop ingestion experiments |
| `sample-data/` | Sample source data |
| `scenarios.json` | Scenario manifest used by shell and Airflow |

## Documentation Map

| Topic | Link |
|---|---|
| Full docs index | [docs/README.md](docs/README.md) |
| Requirements | [Project requirements](docs/requirements.md) |
| Beginner explanation | [Plain-language guide](docs/learning/plain-language-guide.md) |
| Terms and vocabulary | [Glossary](docs/learning/glossary.md) |
| New teammate route | [Onboarding journey](docs/learning/onboarding-journey.md) |
| Architecture | [System overview](docs/architecture/system-overview.md) |
| Data movement | [Data flow](docs/architecture/data-flow.md) |
| Operations | [Runbooks](docs/runbooks/startup-shutdown.md) |
| Scenarios | [Scenario index](docs/scenarios/index.md) |
| Team project model | [Team getting started](docs/team-getting-started.md) |
| External learning links | [References](docs/references.md) |

## Cleanup

Stop containers only:

```bash
make down
```

Remove all POC data and volumes:

```bash
make reset
```
