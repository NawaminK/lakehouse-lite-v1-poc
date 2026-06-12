from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="lakehouse_v1_poc",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["poc", "iceberg", "spark", "trino"],
) as dag:
    create_tables = BashOperator(
        task_id="spark_create_iceberg_tables",
        bash_command="docker exec spark-iceberg spark-submit /home/iceberg/jobs/01_create_tables.py",
    )

    quality_check = BashOperator(
        task_id="spark_quality_check",
        bash_command="docker exec spark-iceberg spark-submit /home/iceberg/jobs/02_quality_check.py",
    )

    trino_validate = BashOperator(
        task_id="trino_validate_gold_table",
        bash_command=(
            "docker exec trino trino --server http://localhost:8080 "
            "--catalog iceberg --schema gold "
            "--execute \"SELECT count(*) AS rows FROM daily_sales\""
        ),
    )

    create_tables >> quality_check >> trino_validate
