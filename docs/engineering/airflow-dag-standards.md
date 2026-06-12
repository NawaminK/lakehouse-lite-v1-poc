# Airflow DAG Standards

These standards keep the POC DAGs easy to read and safe to extend.

## Naming

- DAG IDs should start with `lakehouse_v1_poc`.
- Scenario task IDs should include the scenario number, for example `scenario_04_cdc_merge_upsert`.
- Task IDs should describe the data operation, not the implementation detail only.

## Dependencies

- Prefer a linear DAG for tutorial scenarios.
- Use parallel branches only when the data dependencies are truly independent.
- Validation tasks should run after the data they validate is created.

## Commands

- Spark tasks should call `spark-submit` in the `spark-iceberg` container.
- Trino tasks should call the Trino CLI in the `trino` container.
- Keep shell commands deterministic and avoid interactive prompts.

## Local POC security note

The current DAGs use Docker socket access. That is acceptable for this local POC because it makes the learning path simple. A production deployment should replace this with a proper Airflow executor, packaged Spark jobs, secrets management, and service-level authorization.

## Testing

For DAG changes:

```bash
python -m compileall airflow/dags
make smoke
```

For scenario DAG changes, run:

```bash
make scenarios
```

