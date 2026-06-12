# Scenario Index

The full narrative remains in `docs/poc_test_scenarios.md`. These smaller files make it easier for teammates to run, review, and improve one scenario at a time.

The source of truth for scenario order and automation is `scenarios.json`.

| ID | Scenario | Type | Doc |
|---:|---|---|---|
| 00 | Platform health check | manual | `docs/scenarios/scenario-00-platform-health-check.md` |
| 01 | Base end-to-end table creation | automated | `docs/scenarios/scenario-01-base-end-to-end.md` |
| 02 | Base data quality checks | automated | `docs/scenarios/scenario-02-base-quality-gate.md` |
| 03 | Schema evolution | automated | `docs/scenarios/scenario-03-schema-evolution.md` |
| 04 | CDC merge/upsert | automated | `docs/scenarios/scenario-04-cdc-merge-upsert.md` |
| 05 | Time travel and snapshots | automated | `docs/scenarios/scenario-05-time-travel-snapshots.md` |
| 06 | Partitioning and file layout | automated | `docs/scenarios/scenario-06-partition-file-layout.md` |
| 07 | Expected data quality failure | automated | `docs/scenarios/scenario-07-quality-failure-expected.md` |
| 08 | Iceberg maintenance | automated | `docs/scenarios/scenario-08-iceberg-maintenance.md` |
| 09 | Late arriving data and backfill rebuild | automated | `docs/scenarios/scenario-09-late-arriving-backfill.md` |
| 10 | Trino catalog discovery | automated | `docs/scenarios/scenario-10-trino-catalog-discovery.md` |
| 11 | Trino business queries | automated | `docs/scenarios/scenario-11-trino-business-queries.md` |
| 12 | Trino SQL assertions | automated | `docs/scenarios/scenario-12-trino-sql-assertions.md` |
| 13 | Iceberg metadata inspection through Trino | automated | `docs/scenarios/scenario-13-metadata-inspection.md` |
| 14 | Superset dashboard validation | manual | `docs/scenarios/scenario-14-superset-dashboard-validation.md` |
| 15 | MinIO physical object inspection | manual | `docs/scenarios/scenario-15-minio-physical-object-inspection.md` |
| 16 | Observability smoke test | manual | `docs/scenarios/scenario-16-observability-smoke-test.md` |
| 17 | Failure and recovery drill | manual | `docs/scenarios/scenario-17-failure-recovery-drill.md` |

Run all automated scenarios:

```bash
make scenarios
```

