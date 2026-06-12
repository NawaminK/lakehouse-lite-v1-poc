# Scenario 11: Trino Business Queries

Goal: emulate analyst and BI SQL access through Trino.

Run:

```bash
docker compose exec trino trino --server http://localhost:8080 --file /tmp/sql/scenarios/02_business_queries.sql
```

Queries include:

- Daily sales by date and province.
- Total net sales by province.
- Backfill aggregate by date.
- Active customers by tier.

Pass criteria:

- All queries return results.
- No table or schema lookup errors occur.

