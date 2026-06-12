# Scenario 03: Schema Evolution

Goal: prove an Iceberg table can add nullable columns while old rows remain readable.

Run:

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/03_schema_evolution.py
```

What it demonstrates:

- `ALTER TABLE ADD COLUMNS`.
- Old rows return `NULL` for new columns.
- Iceberg snapshots record the table changes.

Pass criteria:

- Row count is 6.
- Schema includes `coupon_code` and `channel`.
- Snapshot metadata is queryable.

