# Team Getting Started Guide

Use this guide after reading `README.md` and `docs/requirements.md`. It points each team to the minimum docs, commands, files, and starter issues needed to begin.

## Shared Start

```bash
cp .env.example .env
make up
make smoke
make validate
```

Read first:

1. `docs/learning/plain-language-guide.md`
2. `docs/learning/glossary.md`
3. `docs/architecture/system-overview.md`
4. `docs/requirements.md`
5. `docs/github-workflow.md`
6. `docs/engineering/definition-of-done.md`

Expected outcome:

- You can explain the source -> Spark -> Iceberg -> Trino -> Superset path.
- You know your team ownership and related requirement IDs.
- You can open a small PR with validation evidence.

## Team Map

| Team | Focus | Starter issues |
|---|---|---|
| Team A: Platform + Observability | Runtime, DevEx, readiness, metrics | #1, #2, #3, #4 |
| Team B: Lakehouse Core + Data Engineering | Iceberg, Spark, Trino, data quality | #5, #6, #7, #8 |
| Team C: Orchestration + BI | Airflow, backfill, Superset | #9, #10, #11, #12 |
| Team D: AI + Ingestion UX | AI query API, guardrails, NiFi/Hop experiments | #13, #14, #15, #16 |

## Team A: Platform + Observability

Mission: make the local platform easy to run, inspect, and recover.

| Need | Start here |
|---|---|
| Learning docs | `docs/learning/platform-learning-path.md`, `docs/learning/observability-learning-path.md` |
| Runbooks | `docs/runbooks/startup-shutdown.md`, `docs/runbooks/service-health-checklist.md`, `docs/runbooks/troubleshooting.md` |
| Key files | `docker-compose.yml`, `Makefile`, `infra/scripts/wait-for-services.sh`, `prometheus/prometheus.yml`, `monitoring/` |
| Commands | `make up`, `make ps`, `make smoke`, `docker compose ps` |
| Requirements | `PLAT`, `OBS`, `NFR` in `docs/requirements.md` |
| First issues | #1, #2, #3, #4 |

References:

- [Docker Compose](https://docs.docker.com/compose/)
- [Prometheus](https://prometheus.io/docs/introduction/overview/)
- [Grafana](https://grafana.com/docs/grafana/latest/)
- [cAdvisor](https://github.com/google/cadvisor)

## Team B: Lakehouse Core + Data Engineering

Mission: make the data path understandable, queryable, and trustworthy.

| Need | Start here |
|---|---|
| Learning docs | `docs/learning/lakehouse-learning-path.md`, `docs/learning/spark-data-engineering-learning-path.md` |
| Architecture | `docs/architecture/data-flow.md`, `docs/architecture/naming-conventions.md` |
| Key files | `spark/jobs/`, `sample-data/`, `sql/`, `trino/etc/catalog/iceberg.properties` |
| Commands | `make spark-create`, `make spark-quality`, Trino query examples |
| Requirements | `CORE`, `DE`, `NFR` in `docs/requirements.md` |
| First issues | #5, #6, #7, #8 |

Reference command:

```bash
docker compose exec trino trino --server http://localhost:8080 --catalog iceberg --schema gold --execute "SELECT * FROM daily_sales ORDER BY order_dt, province"
```

References:

- [Apache Iceberg](https://iceberg.apache.org/docs/latest/)
- [Iceberg Spark writes](https://iceberg.apache.org/docs/latest/spark-writes/)
- [Apache Spark](https://spark.apache.org/docs/latest/)
- [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html)
- [MinIO](https://docs.min.io/)

## Team C: Orchestration + BI

Mission: make jobs schedulable and gold data usable for BI.

| Need | Start here |
|---|---|
| Learning docs | `docs/learning/airflow-learning-path.md`, `docs/learning/superset-learning-path.md` |
| Standards/runbooks | `docs/engineering/airflow-dag-standards.md`, `docs/runbooks/superset-trino-connection.md` |
| Key files | `airflow/dags/`, `superset/`, `sql/trino_validation.sql` |
| Commands | `make up`, `make spark-create`, `make spark-quality` |
| Requirements | `ORCH`, `BI`, `NFR` in `docs/requirements.md` |
| First issues | #9, #10, #11, #12 |

Open:

- Airflow: http://localhost:8081
- Superset: http://localhost:8088
- Trino: http://localhost:8080

References:

- [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/)
- [Airflow Docker Compose guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Apache Superset](https://superset.apache.org/docs/intro)
- [Superset database connections](https://superset.apache.org/docs/configuration/databases)

## Team D: AI + Ingestion UX

Mission: explore safe AI query access and visual ingestion patterns.

| Need | Start here |
|---|---|
| Learning docs | `docs/learning/ai-learning-path.md`, `ai-assistant/README.md` |
| Safety docs | `docs/security/poc-vs-production.md`, `docs/references.md#ai-and-ml`, `docs/references.md#ingestion-ux` |
| Key files | `ai-assistant/`, `ai-assistant/tests/`, `ingestion/` |
| Commands | AI profile command, AI unit tests |
| Requirements | `AI`, `ING`, `SEC`, `NFR` in `docs/requirements.md` |
| First issues | #13, #14, #15, #16 |

Reference commands:

```bash
make spark-create
make spark-quality
docker compose --profile ai up -d --build ai-assistant
python -m unittest discover -s ai-assistant/tests
```

References:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Trino Python client](https://github.com/trinodb/trino-python-client)
- [Apache NiFi](https://nifi.apache.org/documentation/)
- [Apache Hop](https://hop.apache.org/manual/latest/)

## First PR Rule

Keep the first PR small. Link the issue, include the requirement ID, and paste the narrowest useful validation evidence.
