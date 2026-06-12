# Scenario 08: Iceberg Maintenance

Goal: show why snapshot and file maintenance matters.

Run:

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/08_iceberg_maintenance.py
```

What it demonstrates:

- Many small appends create multiple snapshots.
- Metadata tables expose snapshot and file counts.
- `expire_snapshots` is the intended maintenance pattern where supported.

Pass criteria:

- Snapshot and file metadata queries succeed.
- The script exits successfully even if the local image cannot execute the maintenance procedure.

