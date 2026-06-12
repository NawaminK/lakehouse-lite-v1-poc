# Onboarding Journey

This guide turns the learning paths into a practical route for a new teammate.

## Day 1: Run and observe the baseline

Goal: prove the local platform works and understand the main data path.

```bash
cp .env.example .env
make up
make ps
make smoke
```

Then inspect:

- MinIO Console: `http://localhost:9001`
- Trino: `make trino`
- Superset: `http://localhost:8088`
- Airflow: `http://localhost:8081`
- Prometheus: `http://localhost:9090`

Expected learning outcome:

- You can explain why Spark writes Iceberg tables and Trino reads them.
- You can find the `gold.daily_sales` table from Trino and Superset.
- You know where to look when a service is unhealthy.

## Days 2-3: Trace one data product

Goal: follow one dataset end to end.

1. Read `spark/jobs/01_create_tables.py`.
2. Query `iceberg.bronze.orders_raw`, `iceberg.silver.orders_clean`, and `iceberg.gold.daily_sales`.
3. Open MinIO and find the table `data/` and `metadata/` folders.
4. Read `sql/trino_validation.sql`.
5. Trigger `lakehouse_v1_poc` in Airflow.

Expected learning outcome:

- You can describe bronze/silver/gold responsibilities.
- You can explain what Iceberg metadata adds beyond raw Parquet files.

## Days 4-5: Run the scenario pack

Goal: see real lakehouse behaviors beyond the happy path.

```bash
make scenarios
```

Focus on:

- Schema evolution.
- CDC merge/upsert.
- Time travel.
- Partition/file metadata.
- Late-arriving backfill.

Expected learning outcome:

- You can identify which scenario demonstrates each lakehouse concept.
- You can use Trino metadata tables for debugging.

## Week 2: Make one safe contribution

Pick one issue from `docs/backlog/README.md`.

Recommended first contributions:

- Add a new SQL assertion.
- Add a small Spark validation.
- Add a Superset chart spec.
- Improve a runbook with one reproduced failure.

Before opening a PR:

```bash
make smoke
python -m unittest discover -s ai-assistant/tests
```

Use `docs/engineering/definition-of-done.md` to self-review.
