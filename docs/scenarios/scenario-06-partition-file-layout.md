# Scenario 06: Partitioning and File Layout

Goal: inspect hidden partitioning and physical file metadata.

Run:

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/06_partition_file_layout.py
```

What it demonstrates:

- `PARTITIONED BY (days(order_ts), province)`.
- Iceberg `.files` metadata table.
- Query plan inspection for date and province filters.

Pass criteria:

- Table has 5 rows.
- File metadata includes path, partition, record count, and file size.

