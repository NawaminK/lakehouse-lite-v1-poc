# Scenario 04: CDC Merge/Upsert

Goal: apply insert, update, and delete-like events into a current-state table.

Run:

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/04_cdc_merge_upsert.py
```

What it demonstrates:

- Spark SQL `MERGE INTO`.
- Soft delete via `is_deleted`.
- Current-state dimension style table.

Pass criteria:

- Merge succeeds.
- Active customer count is 3.
- Snapshot metadata shows the write history.

