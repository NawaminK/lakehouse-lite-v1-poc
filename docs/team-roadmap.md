# Team Roadmap

This roadmap describes timing and ownership. Detailed scope lives in `docs/requirements.md`; active work is tracked in GitHub issues and the Project Board.

Planning sources:

- Requirements: `docs/requirements.md`
- Team onboarding: `docs/team-getting-started.md`
- Backlog index: `docs/backlog/README.md`
- Project Board: https://github.com/users/NawaminK/projects/3
- Definition of Done: `docs/engineering/definition-of-done.md`

## Team Structure

| Team | Ownership | Primary paths |
|---|---|---|
| Team A: Platform + Observability | Local runtime, DevEx, service health, metrics | `docker-compose.yml`, `Makefile`, `.github/`, `infra/`, `prometheus/`, `monitoring/` |
| Team B: Lakehouse Core + Data Engineering | MinIO, Iceberg, Spark, Trino, data quality | `spark/`, `sample-data/`, `sql/`, `trino/` |
| Team C: Orchestration + BI | Airflow, backfill, Superset, dashboard practices | `airflow/`, `superset/`, `docs/runbooks/` |
| Team D: AI + Ingestion UX | AI query API, SQL guardrails, NiFi/Hop experiments | `ai-assistant/`, `ingestion/` |

## Phase 1: Stabilize The POC

Target: 2 to 4 weeks.

Outcomes:

- `make up`, `make smoke`, `make validate`, and `make reset` are reliable.
- Spark writes Iceberg tables and Trino reads them.
- Superset connects to Trino and can inspect `iceberg.gold.daily_sales`.
- Airflow triggers the baseline flow.
- Prometheus/Grafana/cAdvisor expose first health signals.
- The AI Assistant remains optional and read-only.
- Each team completes at least one reviewed PR.

Starter work:

- Issues #1-#16 in the Project Board.
- Requirement areas: `PLAT`, `CORE`, `DE`, `ORCH`, `BI`, `OBS`, `AI`, `ING`.

## Phase 2: Add Repeatable Patterns

Target: 1 to 3 months.

Outcomes:

- Reusable ingestion pattern: source -> bronze -> silver -> gold.
- Rejected-record and quality-gate pattern.
- Backfill and recovery runbooks.
- Dashboard import/export practice.
- Observability dashboard v1.
- AI query logging and sample question catalog.

## Phase 3: Evaluate Production-Like Extensions

Target: 3 to 6 months.

Outcomes:

- Separate development, test, and demo profiles if needed.
- Evaluate catalog/governance options such as Polaris, Nessie, OpenMetadata, Ranger, or OPA.
- Evaluate NiFi/Hop visual ingestion integration.
- Evaluate MLflow and Qdrant extensions.
- Document security, backup, restore, and Kubernetes/Helm migration gaps.

## Review Cadence

- Keep issues small and tied to requirement IDs.
- Move work across the Project Board: Todo -> In Progress -> Done.
- Update `docs/requirements.md` only when scope, validation gates, or ownership changes.
- Update this roadmap only when timeline or priorities change.
