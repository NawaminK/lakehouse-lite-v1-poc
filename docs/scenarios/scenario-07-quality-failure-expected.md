# Scenario 07: Expected Data Quality Failure

Goal: prove validation logic catches intentionally bad records.

Run:

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/07_quality_failure_expected.py
```

Expected violations:

- Duplicate order ID.
- Null order ID.
- Null customer ID.
- Negative amount.
- Invalid status.

Pass criteria:

- Every expected violation count is greater than zero.
- Script exits successfully because the failure is expected.

