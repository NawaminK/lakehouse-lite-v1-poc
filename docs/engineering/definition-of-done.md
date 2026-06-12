# Definition of Done

Use this checklist before review. Not every item applies to every PR, but every skipped item should be intentional.

## All changes

- The objective is clear.
- The changed area is owned by the right workstream.
- The PR includes test evidence or explains why runtime testing was not required.
- Documentation is updated when behavior changes.
- No secrets, local generated files, or POC data files are committed.
- Rollback is obvious.

## Platform and DevEx

- `docker compose config` passes.
- `make up`, `make down`, `make smoke`, or the relevant Make target still works.
- New services have documented ports, credentials, health checks, and volumes.
- Image versions are pinned or have a documented reason for floating.

## Lakehouse Core

- Spark, Trino, and Iceberg REST use consistent catalog and S3 settings.
- Namespace/table naming follows `docs/architecture/naming-conventions.md`.
- New metadata behavior includes at least one inspection query.
- Recovery steps are documented for catalog or storage changes.

## Data Engineering and Quality

- New jobs use `spark/jobs/common.py` or document why they cannot.
- Ingestion jobs have bronze, silver, and gold responsibilities clearly separated.
- Quality checks cover required keys, allowed values, nulls, and basic reconciliation.
- Bad-record behavior is documented: fail, quarantine, warn, or ignore.
- A Trino assertion exists when a scenario creates persistent tables.

## Airflow and Operations

- DAG tasks are named with stable, searchable IDs.
- Dependencies match the actual data dependency.
- Retry/backfill behavior is documented when relevant.
- Docker socket use remains limited to this local POC pattern.

## BI and Data Product

- Dataset, metrics, and chart intent are documented.
- SQL uses Trino, not direct object storage access.
- Dashboard validation includes a screenshot, query output, or reproducible checklist.

## Observability

- New dashboards include metric names and expected signal.
- Prometheus targets or Grafana panels are documented.
- Operational runbooks mention which logs or metrics to inspect first.

## AI and Advanced Analytics

- SQL access remains read-only.
- Guardrail tests cover allowed and blocked examples.
- New AI behavior logs or returns failures clearly.
- Production gaps such as authentication, authorization, and audit logging are documented.

