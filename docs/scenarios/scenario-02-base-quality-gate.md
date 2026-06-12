# Scenario 02: Base Data Quality Gate

Goal: prove that a basic quality gate runs before downstream consumption.

Run:

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/02_quality_check.py
```

Checks:

- `silver.orders_clean` has rows.
- `order_id` is not null.
- `amount` is non-negative.
- `status` is one of `paid` or `refund`.

Pass criteria:

- Every rule prints `PASS`.
- Script exits successfully.

