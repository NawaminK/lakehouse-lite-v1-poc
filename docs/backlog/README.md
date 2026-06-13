# Starter Backlog

This file is a compact index. Detailed acceptance criteria live in GitHub issues; durable scope lives in `docs/requirements.md`.

Tracking:

- Project Board: https://github.com/users/NawaminK/projects/3
- Requirements: `docs/requirements.md`
- Team guide: `docs/team-getting-started.md`

## Team A: Platform + Observability

| Issue | Requirement area | Outcome | Evidence |
|---|---|---|---|
| [#1](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/1) Platform smoke and service health | `PLAT`, `OBS` | New teammate can verify local health | `make smoke`, checklist update |
| [#2](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/2) Developer bootstrap diagnostics | `PLAT`, `NFR` | Setup failures are easier to diagnose | diagnostic output, `make validate` |
| [#3](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/3) Grafana dashboard v1 | `OBS` | First container health dashboard | Prometheus query or dashboard evidence |
| [#4](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/4) Service health checklist | `PLAT`, `OBS` | Clear expected health signal per service | `make smoke`, checklist update |

## Team B: Lakehouse Core + Data Engineering

| Issue | Requirement area | Outcome | Evidence |
|---|---|---|---|
| [#5](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/5) Table naming and query examples | `CORE`, `DE` | Layers and table names are explainable | Trino query examples |
| [#6](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/6) Iceberg metadata recovery drill | `CORE`, `NFR` | Metadata debugging path is documented | metadata query evidence |
| [#7](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/7) CSV ingestion template | `DE` | Reusable source -> bronze -> silver -> gold pattern | Spark and Trino evidence |
| [#8](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/8) Rejected records pattern | `DE`, `NFR` | Bad-record behavior is explicit | quality scenario or Spark evidence |

## Team C: Orchestration + BI

| Issue | Requirement area | Outcome | Evidence |
|---|---|---|---|
| [#9](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/9) CSV ingestion DAG | `ORCH`, `DE` | Ingestion can be scheduled | Airflow run or dry-run note |
| [#10](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/10) Backfill runbook | `ORCH`, `NFR` | Date-range reruns are understandable | scenario/query evidence |
| [#11](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/11) Superset dashboard v1 | `BI` | Gold table can support a BI view | screenshot, query, or setup note |
| [#12](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/12) Dashboard import/export practice | `BI`, `NFR` | Dashboard changes are reproducible | export/import note |

## Team D: AI + Ingestion UX

| Issue | Requirement area | Outcome | Evidence |
|---|---|---|---|
| [#13](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/13) Query logging | `AI`, `SEC` | Query behavior can be audited locally | AI unit tests |
| [#14](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/14) Sample question catalog | `AI` | Safe examples exist for demos | allowed and blocked query examples |
| [#15](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/15) NiFi experiment note | `ING` | Visual ingestion idea is scoped | experiment note |
| [#16](https://github.com/NawaminK/lakehouse-lite-v1-poc/issues/16) Hop experiment note | `ING` | Hop handoff to bronze ingestion is scoped | experiment note |

## Backlog Rules

- Add or update GitHub issues first; keep this page as an index.
- Include requirement IDs in issue and PR descriptions.
- Keep acceptance criteria in issues to avoid duplicated stale docs.
- Use the Project Board for status instead of editing this file for status changes.
