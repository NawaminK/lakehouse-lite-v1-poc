# Project Requirements

This document is the source of truth for what Lakehouse Lite v1 POC must support. Use it when creating GitHub issues, reviewing pull requests, planning team work, or deciding whether a change belongs in this repository.

## Requirement Language

- **MUST** means required for the current POC.
- **SHOULD** means strongly recommended, but a PR may document why it is deferred.
- **MAY** means optional or exploratory.
- **Future** means intentionally outside the current local POC.

## Product Goal

Lakehouse Lite v1 POC MUST help a team learn and improve a small open-source lakehouse platform that runs locally on one machine. It MUST demonstrate the path from source data to trusted Iceberg tables, SQL queries, dashboards, orchestration, monitoring, and optional read-only AI access.

## Scope

### In Scope For v1 POC

- Single-node Docker Compose runtime.
- Local MinIO S3-compatible storage.
- Apache Iceberg table format with REST catalog.
- Spark jobs for bronze, silver, and gold tables.
- Trino SQL access to Iceberg tables.
- Superset BI access through Trino.
- Airflow orchestration for baseline jobs and scenarios.
- Prometheus, Grafana, and cAdvisor observability.
- Optional AI Assistant with read-only SQL guardrails.
- Scenario-based validation for lakehouse behavior.
- Team-based learning through docs, issues, PRs, and Project Board tracking.

### Out Of Scope For v1 POC

- Production high availability.
- TLS and production-grade secret management.
- SSO, fine-grained authorization, row-level security, and enterprise audit.
- Distributed object storage or backup/restore guarantees.
- Production Airflow deployment with external metadata database.
- Enterprise data catalog, lineage, governance, and policy enforcement.
- Kubernetes or Helm deployment.

See `docs/security/poc-vs-production.md` for security boundaries.

## Stakeholders And Teams

| Group | Need |
|---|---|
| New teammate | Understand the platform quickly and make one safe contribution |
| Platform operator | Start, stop, inspect, and recover local services |
| Data engineer | Build and validate bronze, silver, and gold data paths |
| Analyst / BI user | Query trusted gold tables and inspect dashboards |
| Reviewer | Check whether a PR meets requirement, validation, and documentation expectations |
| Team A: Platform + Observability | Own local runtime, health checks, metrics, and runbooks |
| Team B: Lakehouse Core + Data Engineering | Own Iceberg, Spark, Trino, table design, and quality |
| Team C: Orchestration + BI | Own Airflow workflows, backfills, Superset, and dashboard practices |
| Team D: AI + Ingestion UX | Own read-only AI query access and ingestion experiments |

## Functional Requirements

| ID | Requirement | Owner | Evidence |
|---|---|---|---|
| PLAT-001 | The platform MUST start with Docker Compose through `make up`. | Team A | `docker compose config`, `make up`, `make ps` |
| PLAT-002 | Common developer commands MUST be discoverable through `make help`. | Team A | `Makefile`, `README.md` |
| PLAT-003 | Required local configuration MUST have safe POC defaults in `.env.example`. | Team A | `.env.example`, `docker-compose.yml` |
| PLAT-004 | Service readiness MUST be checkable through `make smoke` and documented service URLs. | Team A | `make smoke`, `docs/runbooks/service-health-checklist.md` |
| PLAT-005 | Team work MUST be trackable through GitHub issues and the project board. | Team A | [Project Board](https://github.com/users/NawaminK/projects/3), `docs/backlog/README.md` |
| CORE-001 | The lakehouse storage path MUST use MinIO as S3-compatible object storage. | Team B | MinIO console, `docs/scenarios/scenario-15-minio-physical-object-inspection.md` |
| CORE-002 | Tables MUST use Apache Iceberg and be discoverable through the Iceberg REST catalog. | Team B | `spark/jobs/`, `trino/etc/catalog/iceberg.properties` |
| CORE-003 | Trino MUST query Iceberg tables and metadata. | Team B | `sql/trino_validation.sql`, metadata scenarios |
| DE-001 | The baseline pipeline MUST produce bronze, silver, and gold tables. | Team B | `make spark-create`, `docs/architecture/data-flow.md` |
| DE-002 | Data quality checks MUST fail clearly when required business rules are violated. | Team B | `make spark-quality`, scenario 7 |
| DE-003 | Persistent scenario outputs SHOULD include SQL assertions when practical. | Team B | `sql/scenarios/`, scenario 12 |
| DE-004 | New ingestion patterns SHOULD document bad-record behavior: fail, quarantine, warn, or ignore. | Team B | `docs/engineering/definition-of-done.md` |
| ORCH-001 | Airflow MUST run the baseline create -> quality -> validation flow. | Team C | `airflow/dags/`, Airflow UI |
| ORCH-002 | Scenario orchestration SHOULD support repeatable scenario runs. | Team C | `lakehouse_v1_poc_scenarios`, `scenarios.json` |
| ORCH-003 | Backfill and recovery behavior SHOULD be documented before adding new scheduled flows. | Team C | Backfill runbook, scenario 9 |
| BI-001 | Superset MUST connect to Trino with the documented URI. | Team C | `docs/runbooks/superset-trino-connection.md` |
| BI-002 | BI work SHOULD use curated gold tables instead of raw object storage. | Team C | `iceberg.gold.daily_sales`, Superset docs |
| BI-003 | Dashboard changes SHOULD include reproducible setup, screenshot, query output, or export evidence. | Team C | PR evidence, dashboard validation scenario |
| OBS-001 | Prometheus MUST collect local service/container signals. | Team A | `prometheus/prometheus.yml`, scenario 16 |
| OBS-002 | Grafana SHOULD provide a first useful local health dashboard. | Team A | `monitoring/`, issue #3 |
| OBS-003 | Runbooks MUST explain which logs, URLs, or metrics to inspect first. | Team A | `docs/runbooks/` |
| AI-001 | The optional AI Assistant MUST keep SQL access read-only. | Team D | `ai-assistant/`, unit tests |
| AI-002 | AI guardrails MUST block destructive SQL examples. | Team D | `ai-assistant/tests/` |
| AI-003 | AI query examples SHOULD use curated gold tables and document safety limits. | Team D | `docs/learning/ai-learning-path.md`, issue #14 |
| ING-001 | NiFi/Hop ingestion UX work MAY start as documented experiments before runtime integration. | Team D | `ingestion/`, issues #15-#16 |
| DOC-001 | Beginner docs MUST explain the project in plain language. | All teams | `docs/learning/plain-language-guide.md`, `docs/learning/glossary.md` |
| DOC-002 | Team docs MUST show how each team starts learning and contributing. | All teams | `docs/team-getting-started.md`, `docs/team-roadmap.md` |
| DOC-003 | External references MUST point readers to official docs where practical. | All teams | `docs/references.md` |
| SEC-001 | POC security limits MUST be documented and not represented as production-ready. | All teams | `docs/security/poc-vs-production.md` |

## Non-Functional Requirements

| ID | Requirement | Evidence |
|---|---|---|
| NFR-001 | The POC MUST be reproducible on a local machine with Docker Compose. | `make up`, `make smoke` |
| NFR-002 | The repository MUST avoid committed generated files such as `.DS_Store`, `__pycache__`, and `*.pyc`. | `make validate` |
| NFR-003 | Code and config changes MUST include relevant validation evidence. | PR description, `docs/engineering/definition-of-done.md` |
| NFR-004 | Documentation MUST be updated when behavior, commands, ports, or workflows change. | PR diff |
| NFR-005 | New runtime services MUST document port, credentials, health check, volume, and ownership. | README, runbooks, compose config |
| NFR-006 | Secrets and production data MUST NOT be committed. | PR review, `.gitignore`, validation |
| NFR-007 | POC defaults MAY favor learning speed, but production gaps MUST be documented. | `docs/security/poc-vs-production.md` |
| NFR-008 | Scenario docs MUST stay aligned with `scenarios.json`. | `make validate` |
| NFR-009 | Team work MUST remain small enough for review and learning. | GitHub issues, Project Board |
| NFR-010 | AI behavior MUST fail safely and explain blocked queries clearly. | AI tests, API response examples |

## Acceptance Gates

Use the narrowest validation that proves the requirement touched by a change.

| Gate | When to run | Command or evidence |
|---|---|---|
| Repository validation | Every PR | `make validate` |
| Compose validation | Compose or service config changes | `docker compose config` |
| Platform smoke | Runtime/platform changes | `make smoke` |
| Baseline lakehouse path | Spark/Iceberg/Trino changes | `make spark-create`, `make spark-quality`, Trino query evidence |
| Scenario pack | Scenario, DAG, or behavior changes | `make scenarios` or focused scenario command |
| AI tests | AI Assistant changes | `python -m unittest discover -s ai-assistant/tests` |
| Documentation evidence | Docs-only changes | Clear links, updated index, and `make validate` |
| BI evidence | Superset changes | Screenshot, export artifact, or reproducible checklist |
| Observability evidence | Metrics/dashboard changes | Prometheus query, Grafana screenshot, or dashboard JSON |

## Traceability To Current Team Issues

| Team | Requirement areas | Starter issues |
|---|---|---|
| Team A | PLAT, OBS, NFR | #1, #2, #3, #4 |
| Team B | CORE, DE, NFR | #5, #6, #7, #8 |
| Team C | ORCH, BI, NFR | #9, #10, #11, #12 |
| Team D | AI, ING, SEC, NFR | #13, #14, #15, #16 |

Project tracking:

- GitHub Project Board: https://github.com/users/NawaminK/projects/3
- Backlog source: `docs/backlog/README.md`
- Team guide: `docs/team-getting-started.md`

## Issue And PR Expectations

Every issue or PR SHOULD include:

- Requirement ID or a note that the work is exploratory.
- Team owner.
- Scope and out-of-scope notes.
- Acceptance criteria.
- Validation evidence.
- Documentation links.

Feature requests SHOULD use `.github/ISSUE_TEMPLATE/feature_request.md`.

## Change Control

Update this document when:

- A new major capability is added.
- A requirement changes owner or scope.
- A new validation gate becomes required.
- A POC boundary moves closer to production-like behavior.
- A team creates a new recurring class of work.

Keep requirement IDs stable once issues or PRs reference them. If a requirement is retired, mark it as retired instead of reusing the ID for a different purpose.
