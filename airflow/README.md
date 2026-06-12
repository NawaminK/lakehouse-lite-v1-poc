# Airflow

Airflow orchestrates Spark and Trino tasks in this POC.

## URL

http://localhost:8081

Default user: `admin`
Default password: `admin`

## DAGs

- `lakehouse_v1_poc`: baseline pipeline.
- `lakehouse_v1_poc_scenarios`: scenario test pipeline.

## Notes

The POC uses Docker socket access from Airflow to run commands in other containers. This is convenient for local POC work, but it is not a production security pattern.
