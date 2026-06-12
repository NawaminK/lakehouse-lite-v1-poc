# Lakehouse Lite v1 POC Team Roadmap

This document turns the single-node POC into a team-based engineering project. The goal is to make the platform easy to learn, easy to improve, and safe to change through GitHub collaboration.

## Team workstreams

| Team | Main ownership | Primary folders |
|---|---|---|
| Platform and DevEx | Docker Compose, developer workflow, Makefile, GitHub Actions | `docker-compose.yml`, `Makefile`, `.github/`, `infra/` |
| Lakehouse Core | MinIO, Iceberg REST Catalog, Trino Iceberg connector | `minio/`, `iceberg/`, `trino/`, `sql/` |
| Data Engineering and Quality | Spark jobs, ingestion, bronze/silver/gold, quality checks | `spark/`, `sample-data/`, `sql/scenarios/` |
| Orchestration and Operations | Airflow DAGs, retry, backfill, runbooks | `airflow/`, `docs/runbooks/` |
| BI and Data Product | Superset datasets, metrics, charts, dashboards | `superset/`, `docs/learning/superset-learning-path.md` |
| Observability | cAdvisor, Prometheus, Grafana, dashboards, alerts | `prometheus/`, `monitoring/` |
| AI and Advanced Analytics | Read-only Trino query API, text-to-SQL guardrails, RAG/ML extensions | `ai-assistant/` |
| Ingestion UX | NiFi/Hop visual ingestion experiments | `ingestion/` |

## Short-term goals: 2 to 4 weeks

1. Stabilize the baseline POC: Spark writes Iceberg, Trino reads Iceberg, Superset queries Trino, Airflow triggers jobs.
2. Make the repository team-ready: PR template, issue templates, CODEOWNERS, basic CI, Makefile.
3. Add documented runbooks for startup, shutdown, reset, Superset-Trino troubleshooting, and scenario tests.
4. Create a first business dashboard in Superset from `iceberg.gold.daily_sales`.
5. Add a basic monitoring dashboard from cAdvisor metrics in Prometheus/Grafana.
6. Build a read-only AI query API prototype that can query Trino safely.

Expected outputs:

- `make up`, `make smoke`, and `make reset` work.
- GitHub Actions validates syntax and Docker Compose config.
- The team can onboard by reading `docs/learning/*`.
- Each team has at least one closed GitHub issue and one reviewed pull request.
- Pull requests use `docs/engineering/definition-of-done.md`.
- Starter issues are tracked from `docs/backlog/README.md`.

## Medium-term goals: 1 to 3 months

1. Add reusable CSV/API/database ingestion templates.
2. Add data quality and rejected-record patterns for every ingestion job.
3. Add incremental ingestion and CDC/upsert scenarios.
4. Add Iceberg maintenance jobs: expire snapshots, remove orphan files, compact small files where supported.
5. Add dashboard import/export practices for Superset.
6. Add Airflow DAG standards and DAG testing.
7. Add AI text-to-SQL with strict read-only guardrails and query logging.

Expected outputs:

- A repeatable data product template: source -> bronze -> silver -> gold -> dashboard.
- A scenario pack that tests schema evolution, time travel, backfill, and failure recovery.
- A documented path to add a new source system.

## Long-term goals: 3 to 6 months

1. Split development, test, and demo profiles.
2. Add governance components such as OpenMetadata, Keycloak, and Ranger/OPA if required.
3. Evaluate Polaris or Nessie as a production-grade Iceberg catalog option.
4. Add NiFi/Hop for visual ingestion.
5. Add MLflow for model lifecycle and Qdrant for vector search/RAG.
6. Prepare a Kubernetes/Helm migration path if the POC needs to scale.
7. Add backup, restore, disaster recovery, and security baseline runbooks.

## Suggested first GitHub issues

### Platform

- P1-001 Restructure repository for team-based development
- P1-002 Add Makefile for common commands
- P1-003 Add `.env.example` and secret handling guideline
- P1-004 Add GitHub Actions basic CI
- P1-005 Add CODEOWNERS and PR template

### Lakehouse Core

- L1-001 Stabilize Spark to Iceberg to Trino read/write path
- L1-002 Document Iceberg catalog/schema/table naming convention
- L1-003 Add Trino validation SQL scripts
- L1-004 Document table/view metadata recovery steps
- L1-005 Add Iceberg metadata inspection examples

### Data Engineering

- D1-001 Add CSV ingestion Spark job template
- D1-002 Add rejected records table
- D1-003 Add bronze/silver/gold sample pipeline
- D1-004 Add data quality validation script
- D1-005 Add sample data catalog

### Airflow

- A1-001 Create baseline DAG for create -> quality -> validate
- A1-002 Create CSV ingestion DAG
- A1-003 Add Airflow troubleshooting runbook
- A1-004 Add retry/backfill examples

### BI

- B1-001 Create Superset dataset for daily_sales
- B1-002 Create Lakehouse POC Dashboard v1
- B1-003 Define metrics: net_sales, paid_order_count, refund_count
- B1-004 Add Superset setup guide

### Observability

- O1-001 Verify cAdvisor -> Prometheus -> Grafana flow
- O1-002 Create container metrics dashboard
- O1-003 Add PromQL examples
- O1-004 Add service health checklist

### AI

- AI1-001 Create read-only AI query API through Trino
- AI1-002 Add SQL safety validator
- AI1-003 Add sample questions and SQL templates
- AI1-004 Add query logging table/file
- AI1-005 Document AI guardrails
