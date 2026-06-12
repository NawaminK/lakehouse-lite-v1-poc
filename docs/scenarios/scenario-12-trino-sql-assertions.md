# Scenario 12: Trino SQL Assertions

Goal: use SQL as a lightweight scenario smoke test.

Run:

```bash
docker compose exec trino trino --server http://localhost:8080 --file /tmp/sql/scenarios/03_scenario_assertions.sql
```

Pass criteria:

- Every row in the assertion result has `PASS`.
- Backfill totals and CDC counts match expected values.

