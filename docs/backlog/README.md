# Starter Backlog

These issues are sized for a team learning the platform. Each item should become a GitHub issue before implementation.

## Team A: Platform + Observability

Team A owns local runtime, developer workflow, health checks, and monitoring.

### P1-001 Add repository hygiene checks

Acceptance criteria:

- CI fails if `.DS_Store`, `__pycache__`, or `*.pyc` files are present.
- README or CONTRIBUTING explains generated files must not be committed.
- Validation command is documented.

### P1-002 Add developer bootstrap diagnostics

Acceptance criteria:

- A script verifies Docker, Docker Compose, available memory, and required ports.
- Output is actionable for new teammates.
- The script is linked from the startup runbook.

### O1-001 Build Grafana container dashboard v1

Acceptance criteria:

- Dashboard uses Prometheus/cAdvisor metrics.
- Panels include CPU, memory, network, and filesystem signals.
- Dashboard JSON is stored under `monitoring/grafana`.

### O1-002 Add service health checklist

Acceptance criteria:

- Checklist covers MinIO, Iceberg REST, Spark, Trino, Superset, Airflow, Prometheus, Grafana, and cAdvisor.
- Each service has a URL or command check.

## Team B: Lakehouse Core + Data Engineering

Team B owns object storage, Iceberg tables, Spark transformations, Trino queries, and data quality.

### L1-001 Add table naming convention examples

Acceptance criteria:

- Bronze/silver/gold naming examples are documented.
- Scenario namespace rules are documented.
- At least one Trino query shows each layer.

### L1-002 Add Iceberg metadata recovery drill

Acceptance criteria:

- Runbook explains how to identify bad views/tables.
- Commands exist for safe local reset.
- Scenario test evidence is included.

### D1-001 Add CSV ingestion template

Acceptance criteria:

- Template reads a CSV file from `sample-data/csv`.
- Template writes bronze, silver, and gold tables.
- Template includes validation and rejected-record behavior.
- Trino assertion query is included or referenced.

### D1-002 Add rejected records pattern

Acceptance criteria:

- Bad rows are written to an Iceberg rejected table.
- Good rows continue to silver only when quality policy allows it.
- Documentation explains fail vs quarantine trade-offs.

## Team C: Orchestration + BI

Team C owns workflow scheduling, backfill behavior, Superset datasets, and dashboard practices.

### A1-001 Add CSV ingestion DAG

Acceptance criteria:

- DAG runs the CSV ingestion template.
- DAG includes a validation task.
- DAG follows `docs/engineering/airflow-dag-standards.md`.

### A1-002 Add backfill runbook

Acceptance criteria:

- Runbook explains rerunning a date range.
- Late-arriving data scenario is referenced.
- Recovery and validation commands are included.

### B1-001 Build Superset dashboard v1

Acceptance criteria:

- Dashboard uses `iceberg.gold.daily_sales`.
- Metrics include total net sales and total orders.
- Validation evidence is attached to the PR.

### B1-002 Add dashboard import/export practice

Acceptance criteria:

- Exported assets are stored under `superset/assets`.
- Restore/import steps are documented.
- Ownership for certified datasets is documented.

## Team D: AI + Ingestion UX

Team D owns the read-only AI query API, SQL guardrails, sample questions, and visual ingestion experiments.

### AI1-001 Add query logging

Acceptance criteria:

- `/query` records normalized SQL, status, row count, and error message.
- Logging avoids storing secrets.
- Tests cover success and blocked SQL.

### AI1-002 Add sample question catalog

Acceptance criteria:

- Natural-language questions map to safe SQL examples.
- Examples use `gold.daily_sales`.
- Guardrail behavior is documented.

### UX1-001 Add first NiFi ingestion experiment note

Acceptance criteria:

- `ingestion/` contains a short experiment note or placeholder.
- The note names one input, one expected output table, and one validation idea.
- The experiment links to the Team D getting started guide.

### UX1-002 Add first Hop pipeline experiment note

Acceptance criteria:

- `ingestion/` contains a short experiment note or placeholder.
- The note explains how Hop could fit before bronze ingestion.
- The experiment links to the Team D getting started guide.
