# Startup and Shutdown Runbook

## Prerequisites

- Ubuntu 24.04 or compatible Linux host.
- Docker Engine and Docker Compose v2.
- At least 8 CPU cores, 16 GB RAM, and 50 GB disk for comfortable POC work.

## First start

```bash
cp .env.example .env
export AIRFLOW_UID=$(id -u)
export DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)
make up
make ps
```

## Health check

```bash
make smoke
```

For a service-by-service checklist, see:

```text
docs/runbooks/service-health-checklist.md
```

## Service URLs

| Service | URL | Default credential |
|---|---|---|
| MinIO Console | http://localhost:9001 | admin / password |
| Iceberg REST Catalog | http://localhost:8181 | none |
| Spark/Jupyter | http://localhost:8888 | check container logs if token is required |
| Trino | http://localhost:8080 | none in POC |
| Superset | http://localhost:8088 | admin / admin |
| Airflow | http://localhost:8081 | admin / admin |
| Prometheus | http://localhost:9090 | none |
| Grafana | http://localhost:3000 | admin / admin |
| cAdvisor | http://localhost:8090 | none |

## Stop services

```bash
make down
```

## Reset all POC data

This removes Docker volumes and generated local folders.

```bash
make reset
make up
```

## Common logs

```bash
docker compose logs -f trino
docker compose logs -f spark-iceberg
docker compose logs -f superset
docker compose logs -f airflow
```
