# Lakehouse Lite v1 POC

This repository is a single-node, open-source Lakehouse POC for Ubuntu 24.04 and Docker Compose.

Core data path:

```text
MinIO S3-compatible storage
  -> Apache Iceberg REST Catalog
  -> Spark writes Iceberg tables
  -> Trino queries Iceberg tables
  -> Superset dashboards
  -> Airflow orchestration
  -> Prometheus/Grafana/cAdvisor monitoring
```

The project has been reorganized for team-based learning and development through GitHub issues, pull requests, CODEOWNERS, and CI checks.

## Service URLs

| Service | URL | Default credential |
|---|---|---|
| MinIO API | http://localhost:9000 | none |
| MinIO Console | http://localhost:9001 | admin / password |
| Iceberg REST Catalog | http://localhost:8181 | none |
| Spark/Jupyter | http://localhost:8888 | check logs if token is required |
| Trino | http://localhost:8080 | none |
| Superset | http://localhost:8088 | admin / admin |
| Airflow | http://localhost:8081 | admin / admin |
| Prometheus | http://localhost:9090 | none |
| Grafana | http://localhost:3000 | admin / admin |
| cAdvisor | http://localhost:8090 | none |
| AI Assistant, optional | http://localhost:8010 | none |

## Quick start

```bash
cp .env.example .env
make up
make ps
make smoke
```

Equivalent raw command:

```bash
export AIRFLOW_UID=$(id -u)
export DOCKER_GID=$(stat -c '%g' /var/run/docker.sock 2>/dev/null || stat -f '%g' /var/run/docker.sock 2>/dev/null || echo 999)
docker compose up -d --build
```

## Common commands

```bash
make help
make up
make down
make ps
make logs
make smoke
make scenarios
make validate
make reset
```

## Baseline validation

```bash
make spark-create
make spark-quality
docker compose exec trino trino --server http://localhost:8080 --catalog iceberg --schema gold --execute "SELECT * FROM daily_sales ORDER BY order_dt, province"
```

## Superset connection

Use this URI first:

```text
trino://admin@trino:8080/iceberg
```

Then select schema `gold` and table `daily_sales`.

If the Trino driver has issues, see:

```text
docs/runbooks/superset-trino-connection.md
```

## Airflow

Open http://localhost:8081 and trigger:

- `lakehouse_v1_poc`
- `lakehouse_v1_poc_scenarios`

This POC uses Docker socket access from Airflow. This is convenient for local POC work but is not a production security pattern.

## Extended POC scenarios

Detailed scenario documentation:

```text
docs/poc_test_scenarios.md
```

Run all scenarios:

```bash
make scenarios
```

Scenario coverage includes base pipeline, data quality, schema evolution, CDC upsert, time travel, partition/file layout, expected failure, Iceberg maintenance, late-arriving backfill, Trino assertions, metadata inspection, Superset validation, MinIO inspection, observability, and recovery drill.

## Optional AI query API

Start the AI Assistant profile:

```bash
docker compose --profile ai up -d --build ai-assistant
```

Query through Trino safely:

```bash
curl -X POST http://localhost:8010/query \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT province, SUM(net_sales) AS total_net_sales FROM daily_sales GROUP BY province ORDER BY total_net_sales DESC"}'
```

See:

```text
ai-assistant/README.md
```

## Team-based development

Start here:

```text
CONTRIBUTING.md
docs/README.md
docs/learning/onboarding-journey.md
docs/team-roadmap.md
docs/github-workflow.md
docs/references.md
docs/learning/
docs/runbooks/
```

Recommended workstreams:

1. Platform and DevEx.
2. Lakehouse Core.
3. Data Engineering and Quality.
4. Orchestration and Operations.
5. BI and Data Product.
6. Observability.
7. AI and Advanced Analytics.
8. Ingestion UX.

## Repository map

```text
.github/              GitHub workflow, templates, CODEOWNERS
infra/scripts/        POC automation scripts
docs/                 Architecture, runbooks, learning path, roadmap
spark/jobs/           Spark ETL and scenario jobs
trino/etc/            Trino configuration
sql/                  Trino validation and scenario SQL
airflow/dags/         Airflow DAGs
superset/             Superset image and BI notes
prometheus/           Prometheus config
monitoring/           Monitoring docs and future dashboards
ai-assistant/         Optional read-only Trino query API
ingestion/            Optional NiFi/Hop experiments
sample-data/          Sample source data
scenarios.json        Scenario manifest used by shell and Airflow
```

## Cleanup

Stop containers only:

```bash
make down
```

Remove all POC data and volumes:

```bash
make reset
```
