# Lakehouse Lite v1 POC

Single-node, open-source lakehouse proof of concept for learning how a modern data platform works end to end with Docker Compose.

The POC demonstrates:

- Spark writes bronze, silver, and gold Iceberg tables.
- MinIO stores data and metadata through an S3-compatible API.
- Trino serves SQL over Iceberg tables.
- Superset reads curated gold tables for BI.
- Airflow orchestrates jobs and scenario runs.
- Prometheus, Grafana, and cAdvisor expose local health signals.
- The optional AI Assistant provides guarded, read-only SQL access.

## Architecture

```text
Source data
  -> Spark jobs
  -> Apache Iceberg tables
  -> MinIO object storage
  -> Trino SQL serving
  -> Superset dashboards
  -> Airflow orchestration
  -> Prometheus/Grafana/cAdvisor monitoring
  -> Optional AI Assistant
```

<img width="1536" height="1024" alt="Lakehouse Lite architecture" src="https://github.com/user-attachments/assets/a13209ca-ed0d-40dd-bc52-45ac34d32fee" />

Architecture docs:

- [System overview](docs/architecture/system-overview.md)
- [Data flow](docs/architecture/data-flow.md)
- [Component responsibility](docs/architecture/component-responsibility.md)
- [Naming conventions](docs/architecture/naming-conventions.md)

## Quick Start

```bash
cp .env.example .env
make up
make ps
make smoke
```

Baseline data validation:

```bash
make spark-create
make spark-quality
docker compose exec trino trino --server http://localhost:8080 --catalog iceberg --schema gold --execute "SELECT * FROM daily_sales ORDER BY order_dt, province"
```

Run all POC scenarios:

```bash
make scenarios
```

## Service URLs

| Service | URL | Default credential |
|---|---|---|
| MinIO API | http://localhost:9000 | none |
| MinIO Console | http://localhost:9001 | admin / password |
| Iceberg REST Catalog | http://localhost:8181 | none |
| Spark/Jupyter | http://localhost:8888 | check logs if token is required |
| Trino | http://localhost:8080 | none |
| Superset | http://localhost:8088 | admin / admin |
| Airflow | http://localhost:8081 | admin / admin |
| Prometheus | http://localhost:9090 | none |
| Grafana | http://localhost:3000 | admin / admin |
| cAdvisor | http://localhost:8090 | none |
| AI Assistant, optional | http://localhost:8010 | none |

## Common Commands

| Command | Purpose |
|---|---|
| `make help` | Show available Make targets |
| `make up` | Build/start the local stack |
| `make down` | Stop containers |
| `make ps` | Show container status |
| `make logs` | Tail logs |
| `make smoke` | Check platform readiness |
| `make validate` | Run repository validation and unit tests |
| `make scenarios` | Run the scenario pack |
| `make reset` | Remove POC data and volumes |

## Start Here

| Need | Link |
|---|---|
| Plain-language explanation | [Plain-language guide](docs/learning/plain-language-guide.md) |
| Terms and vocabulary | [Glossary](docs/learning/glossary.md) |
| Full documentation index | [Docs index](docs/README.md) |
| Scope and acceptance gates | [Project requirements](docs/requirements.md) |
| New teammate route | [Onboarding journey](docs/learning/onboarding-journey.md) |
| Team-specific learning path | [Team getting started](docs/team-getting-started.md) |
| External references | [References](docs/references.md) |

## Planning And Contribution

| Area | Link |
|---|---|
| Requirements | [docs/requirements.md](docs/requirements.md) |
| Team roadmap | [docs/team-roadmap.md](docs/team-roadmap.md) |
| Starter backlog index | [docs/backlog/README.md](docs/backlog/README.md) |
| Project board | [Lakehouse Lite Team Kanban](https://github.com/users/NawaminK/projects/3) |
| GitHub workflow | [docs/github-workflow.md](docs/github-workflow.md) |
| Definition of Done | [docs/engineering/definition-of-done.md](docs/engineering/definition-of-done.md) |
| Contributing guide | [CONTRIBUTING.md](CONTRIBUTING.md) |

## Team Tracks

| Team | Focus | First stop |
|---|---|---|
| Team A: Platform + Observability | Docker Compose, Makefile, readiness, Prometheus, Grafana, cAdvisor | [Team A guide](docs/team-getting-started.md#team-a-platform--observability) |
| Team B: Lakehouse Core + Data Engineering | MinIO, Iceberg, Spark, Trino, data quality | [Team B guide](docs/team-getting-started.md#team-b-lakehouse-core--data-engineering) |
| Team C: Orchestration + BI | Airflow, backfills, Superset, dashboards | [Team C guide](docs/team-getting-started.md#team-c-orchestration--bi) |
| Team D: AI + Ingestion UX | AI query API, SQL guardrails, NiFi/Hop experiments | [Team D guide](docs/team-getting-started.md#team-d-ai--ingestion-ux) |

## Repository Map

| Path | Purpose |
|---|---|
| `.github/` | CI, issue templates, PR template, CODEOWNERS |
| `docs/` | Requirements, architecture, runbooks, learning paths |
| `spark/jobs/` | Spark ETL and scenario jobs |
| `sql/` | Trino validation and scenario SQL |
| `trino/etc/` | Trino and Iceberg catalog config |
| `airflow/dags/` | Airflow DAGs |
| `superset/` | Superset setup |
| `prometheus/`, `monitoring/` | Metrics config and dashboards |
| `ai-assistant/` | Optional read-only query API |
| `ingestion/` | Optional NiFi/Hop experiments |
| `sample-data/` | Sample source data |
| `scenarios.json` | Scenario manifest |

## Cleanup

```bash
make down
make reset
```
