# Team Getting Started Guide

This guide splits the project into four learning teams. Each team should be able to start from the same baseline, then focus on its own tools, folders, scenarios, and references.

## Shared Start For Every Team

Do this once before choosing a team task:

```bash
cp .env.example .env
make up
make smoke
make validate
```

Read these first:

1. `README.md`
2. `docs/learning/plain-language-guide.md`
3. `docs/learning/glossary.md`
4. `docs/architecture/system-overview.md`
5. `docs/github-workflow.md`
6. `docs/engineering/definition-of-done.md`

Expected shared outcome:

- You can explain the source -> Spark -> Iceberg -> Trino -> Superset path.
- You know how to start, validate, and reset the local POC.
- You know which team owns which part of the platform.
- You can open a small pull request with evidence from `make validate` or a focused scenario.

## Team Map

| Team | Project focus | Primary outcome |
|---|---|---|
| Team A: Platform + Observability | Local runtime, developer experience, health checks, metrics, dashboards | The POC is easy to run, debug, and monitor |
| Team B: Lakehouse Core + Data Engineering | MinIO, Iceberg, Spark, Trino, bronze/silver/gold, quality checks | Data is stored, transformed, validated, and queryable |
| Team C: Orchestration + BI | Airflow workflows, backfills, Superset datasets, dashboard practices | Pipelines run in order and business users can inspect gold data |
| Team D: AI + Ingestion UX | Read-only query API, SQL guardrails, sample questions, NiFi/Hop experiments | New data entry points and AI-assisted access are explored safely |

## Team A: Platform + Observability

### Mission

Make the local platform boring to operate: start it, check it, inspect it, monitor it, and recover it when something fails.

### Start Here

Read:

1. `docs/learning/platform-learning-path.md`
2. `docs/learning/observability-learning-path.md`
3. `docs/runbooks/startup-shutdown.md`
4. `docs/runbooks/service-health-checklist.md`
5. `docs/runbooks/troubleshooting.md`

Run:

```bash
make up
make ps
make smoke
docker compose ps
```

Inspect:

- `docker-compose.yml`
- `Makefile`
- `infra/scripts/wait-for-services.sh`
- `prometheus/prometheus.yml`
- `monitoring/`

First practice tasks:

- Add one clearer readiness check or troubleshooting note.
- Add one Prometheus query example for a service or container signal.
- Improve the service health checklist with exact expected output.
- Reproduce one failure and document the recovery steps.

Reference links:

- [Docker Compose documentation](https://docs.docker.com/compose/)
- [Prometheus overview](https://prometheus.io/docs/introduction/overview/)
- [Prometheus cAdvisor guide](https://prometheus.io/docs/guides/cadvisor/)
- [Grafana documentation](https://grafana.com/docs/grafana/latest/)
- [cAdvisor project](https://github.com/google/cadvisor)

## Team B: Lakehouse Core + Data Engineering

### Mission

Make the data path understandable and trustworthy: source files become Iceberg tables, Spark transformations are clear, Trino queries work, and data quality checks fail loudly when needed.

### Start Here

Read:

1. `docs/learning/lakehouse-learning-path.md`
2. `docs/learning/spark-data-engineering-learning-path.md`
3. `docs/architecture/data-flow.md`
4. `docs/architecture/naming-conventions.md`
5. `docs/poc_test_scenarios.md`

Run:

```bash
make spark-create
make spark-quality
docker compose exec trino trino --server http://localhost:8080 --execute "SHOW SCHEMAS FROM iceberg"
docker compose exec trino trino --server http://localhost:8080 --catalog iceberg --schema gold --execute "SELECT * FROM daily_sales ORDER BY order_dt, province"
```

Inspect:

- `spark/jobs/01_create_tables.py`
- `spark/jobs/02_quality_checks.py`
- `spark/jobs/scenarios/`
- `sql/trino_validation.sql`
- `sql/scenarios/`
- `sample-data/`
- `trino/etc/catalog/iceberg.properties`

First practice tasks:

- Add one SQL assertion for `gold.daily_sales`.
- Add one data quality check in Spark.
- Document one Iceberg metadata query and explain what it proves.
- Add a small sample dataset and show its bronze/silver/gold path.

Reference links:

- [Apache Iceberg documentation](https://iceberg.apache.org/docs/latest/)
- [Iceberg Spark quickstart](https://iceberg.apache.org/spark-quickstart/)
- [Iceberg Spark writes](https://iceberg.apache.org/docs/latest/spark-writes/)
- [Apache Spark documentation](https://spark.apache.org/docs/latest/)
- [Spark SQL and DataFrames](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html)
- [Trino S3-compatible storage](https://trino.io/docs/current/object-storage/file-system-s3.html)
- [MinIO documentation](https://docs.min.io/)

## Team C: Orchestration + BI

### Mission

Make the platform usable as a product: Airflow runs jobs in a clear order, backfills are understandable, Superset connects to Trino, and dashboards expose trusted gold metrics.

### Start Here

Read:

1. `docs/learning/airflow-learning-path.md`
2. `docs/learning/superset-learning-path.md`
3. `docs/engineering/airflow-dag-standards.md`
4. `docs/runbooks/superset-trino-connection.md`
5. `docs/scenarios/scenario-14-superset-dashboard-validation.md`

Run:

```bash
make up
make spark-create
make spark-quality
```

Then open:

- Airflow: `http://localhost:8081`
- Superset: `http://localhost:8088`
- Trino: `http://localhost:8080`

Inspect:

- `airflow/dags/`
- `sql/trino_validation.sql`
- `superset/`
- `docs/runbooks/superset-trino-connection.md`
- `docs/scenarios/scenario-09-late-arriving-backfill.md`

First practice tasks:

- Trigger `lakehouse_v1_poc` in Airflow and capture validation evidence.
- Add a small DAG note that explains task order and failure behavior.
- Create or document one Superset chart from `iceberg.gold.daily_sales`.
- Improve the backfill runbook with one command and one expected result.

Reference links:

- [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/)
- [Airflow Docker Compose guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Trino with Airflow example](https://trino.io/blog/2022/07/13/how-to-use-airflow-to-schedule-trino-jobs.html)
- [Apache Superset intro](https://superset.apache.org/docs/intro)
- [Superset database connections](https://superset.apache.org/docs/configuration/databases)
- [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html)

## Team D: AI + Ingestion UX

### Mission

Explore safer ways for people and systems to enter the platform: read-only AI query access, SQL guardrails, sample questions, and future visual ingestion paths.

### Start Here

Read:

1. `docs/learning/ai-learning-path.md`
2. `ai-assistant/README.md`
3. `docs/security/poc-vs-production.md`
4. `docs/references.md#ingestion-ux`
5. `docs/references.md#ai-and-ml`

Run:

```bash
make spark-create
make spark-quality
docker compose --profile ai up -d --build ai-assistant
curl -X POST http://localhost:8010/query \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT province, SUM(net_sales) AS total_net_sales FROM daily_sales GROUP BY province ORDER BY total_net_sales DESC"}'
python -m unittest discover -s ai-assistant/tests
```

Inspect:

- `ai-assistant/`
- `ai-assistant/tests/`
- `ingestion/`
- `docs/learning/ai-learning-path.md`
- `docs/security/poc-vs-production.md`

First practice tasks:

- Add one safe natural-language question and matching SQL example.
- Add one AI query validator test for blocked SQL.
- Document what read-only means for the AI assistant.
- Create a short proposal for one NiFi or Hop ingestion experiment.

Reference links:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Trino Python client](https://github.com/trinodb/trino-python-client)
- [Apache NiFi documentation](https://nifi.apache.org/documentation/)
- [Apache Hop user manual](https://hop.apache.org/manual/latest/)
- [MLflow Model Registry](https://mlflow.org/docs/latest/ml/model-registry)
- [Qdrant documentation](https://qdrant.tech/documentation/)

## First Pull Request Checklist

Every team should keep the first PR small. A good first PR changes one doc, one validation check, one scenario note, or one tiny test.

Before opening a PR:

```bash
make validate
```

If your change touches running services, also run the most relevant command:

- Team A: `make smoke`
- Team B: `make spark-create` and `make spark-quality`
- Team C: trigger the relevant Airflow DAG or validate the Superset connection
- Team D: `python -m unittest discover -s ai-assistant/tests`

Attach the command output or a short evidence note to the PR.
