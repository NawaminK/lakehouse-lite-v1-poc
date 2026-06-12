import json
import os
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator

SPARK = "docker exec spark-iceberg spark-submit"
TRINO = "docker exec trino trino --server http://localhost:8080"
MANIFEST_CANDIDATES = [
    Path(os.environ.get("SCENARIO_MANIFEST", "/opt/airflow/scenarios.json")),
    Path(__file__).resolve().parents[2] / "scenarios.json",
]


def load_scenarios() -> list[dict]:
    for manifest_path in MANIFEST_CANDIDATES:
        if manifest_path.exists():
            with manifest_path.open(encoding="utf-8") as fh:
                return json.load(fh)["scenarios"]
    candidates = ", ".join(str(path) for path in MANIFEST_CANDIDATES)
    raise FileNotFoundError(f"Scenario manifest not found. Checked: {candidates}")


def scenario_command(scenario: dict) -> str:
    executor = scenario["executor"]
    if executor == "spark":
        return f"{SPARK} {scenario['path']}"
    if executor == "trino_file":
        return f"{TRINO} --file {scenario['path']}"
    raise ValueError(f"Unsupported Airflow scenario executor: {executor}")

with DAG(
    dag_id="lakehouse_v1_poc_scenarios",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["poc", "iceberg", "scenarios", "spark", "trino"],
) as dag:
    previous_task = None

    for scenario in load_scenarios():
        if not scenario.get("airflow"):
            continue

        task = BashOperator(
            task_id=f"scenario_{scenario['id']}_{scenario['slug']}",
            bash_command=scenario_command(scenario),
        )

        if previous_task:
            previous_task >> task

        previous_task = task
