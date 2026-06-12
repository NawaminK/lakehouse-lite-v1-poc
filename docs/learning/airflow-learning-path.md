# Airflow Learning Path

## Goal

Use Airflow to orchestrate Spark and Trino tasks.

## Concepts

- DAG.
- Task.
- Operator.
- Dependency.
- Retry.
- Backfill.
- Logs.

## Hands-on tasks

- Open Airflow at http://localhost:8081.
- Trigger `lakehouse_v1_poc`.
- Trigger `lakehouse_v1_poc_scenarios`.
- Clear a failed task and rerun downstream tasks.
- Add a validation task that runs a Trino query.

## Key files

- `airflow/dags/lakehouse_v1_poc_dag.py`
- `airflow/dags/lakehouse_v1_poc_scenarios_dag.py`
