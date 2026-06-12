# Scenario 13: Iceberg Metadata Inspection Through Trino

Goal: inspect Iceberg snapshots, history, and files through Trino.

Run:

```bash
docker compose exec trino trino --server http://localhost:8080 --file /tmp/sql/scenarios/04_metadata_inspection.sql
```

Metadata tables:

- `<table>$snapshots`
- `<table>$history`
- `<table>$files`

Pass criteria:

- Snapshot IDs, operations, and file paths are visible.
- Metadata queries complete without errors.

