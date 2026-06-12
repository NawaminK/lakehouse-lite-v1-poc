# Scenario 05: Time Travel and Snapshots

Goal: read an older table version by Iceberg snapshot ID.

Run:

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/05_time_travel_snapshots.py
```

What it demonstrates:

- Snapshot capture after writes.
- Current table read.
- Historical table read with `snapshot-id`.

Pass criteria:

- Current table has 4 rows.
- First snapshot read has 2 rows.

