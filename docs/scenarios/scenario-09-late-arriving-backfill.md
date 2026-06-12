# Scenario 09: Late Arriving Data and Backfill Rebuild

Goal: rebuild a gold aggregate deterministically after late data arrives.

Run:

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/09_late_arriving_backfill.py
```

What it demonstrates:

- Initial bronze load.
- Gold aggregate creation.
- Late batch append.
- Gold table rebuild from bronze.

Pass criteria:

- Gold aggregate has 4 rows.
- Total net sales is 670.00.
- Bangkok 2026-06-10 net sales is 280.00 with 3 orders.

