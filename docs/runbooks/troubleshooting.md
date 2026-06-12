# Troubleshooting Runbook

## Quick diagnosis matrix

| Symptom | Likely area | First command | Common fix |
|---|---|---|---|
| `make smoke` cannot reach MinIO | Object storage | `docker compose logs -f minio` | Check port 9000/9001 and restart MinIO |
| Spark writes fail with S3 errors | MinIO or Iceberg config | `curl http://localhost:8181/v1/config` | Confirm MinIO is healthy and catalog endpoint matches Spark config |
| Trino cannot see Iceberg tables | Trino catalog or Iceberg REST | `docker compose exec trino trino --server http://localhost:8080 --execute "SHOW CATALOGS"` | Restart Trino after catalog config changes |
| Superset connection fails | Docker networking or driver | `docker compose exec -T superset /app/.venv/bin/python -c "import trino, sqlalchemy_trino"` | Use `trino://admin@trino:8080/iceberg`, not localhost |
| Airflow task cannot run Docker | Docker socket permissions | `docker compose logs -f airflow` | Set `AIRFLOW_UID` and `DOCKER_GID` before `make up` |
| Scenario docs and scripts disagree | Scenario manifest drift | `python3 scripts/validate_repo_structure.py` | Update `scenarios.json` and per-scenario docs together |
| Generated files appear in PR | Local cache files | `find . -name __pycache__ -o -name '*.pyc' -o -name .DS_Store` | Remove generated files and run `make validate` |

## Superset cannot connect to Trino

1. Check network from Superset to Trino:

```bash
docker compose exec -T superset /app/.venv/bin/python - <<'PY'
import socket
s = socket.create_connection(("trino", 8080), timeout=5)
print("Superset can connect to Trino")
s.close()
PY
```

2. Check Trino SQLAlchemy driver inside the Superset runtime environment:

```bash
docker compose exec -T superset /app/.venv/bin/python - <<'PY'
import trino
import sqlalchemy_trino
print("Trino driver OK")
PY
```

3. Test SQLAlchemy:

```bash
docker compose exec -T superset /app/.venv/bin/python - <<'PY'
from sqlalchemy import create_engine, text
engine = create_engine("trino://admin@trino:8080/iceberg/gold")
with engine.connect() as conn:
    print(conn.execute(text("SHOW TABLES")).fetchall())
PY
```

4. Use this Superset URI first:

```text
trino://admin@trino:8080/iceberg
```

Then select schema `gold` inside SQL Lab or dataset creation.

## Trino sees a view but cannot load table metadata

Run:

```bash
docker compose exec trino trino --server http://localhost:8080 --execute "SELECT table_schema, table_name, table_type FROM iceberg.information_schema.tables WHERE table_schema = 'gold'"
```

If an object is a bad view, drop it and recreate baseline tables:

```bash
docker compose exec trino trino --server http://localhost:8080 --execute "DROP VIEW IF EXISTS iceberg.gold.daily_sales"
docker compose exec trino trino --server http://localhost:8080 --execute "DROP TABLE IF EXISTS iceberg.gold.daily_sales"
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/01_create_tables.py
```

## Spark writes data but Trino cannot see the table

1. Confirm Iceberg REST catalog is reachable:

```bash
curl http://localhost:8181/v1/config
```

2. Confirm Trino catalog is loaded:

```bash
docker compose exec trino trino --server http://localhost:8080 --execute "SHOW CATALOGS"
```

3. Check `trino/etc/catalog/iceberg.properties` and restart Trino if the file changed:

```bash
docker compose restart trino
```

## Airflow task fails with Docker command error

The POC Airflow DAGs use Docker socket access. Ensure these variables are set before starting Airflow:

```bash
export AIRFLOW_UID=$(id -u)
export DOCKER_GID=$(stat -c '%g' /var/run/docker.sock 2>/dev/null || stat -f '%g' /var/run/docker.sock 2>/dev/null || echo 999)
docker compose up -d airflow
```
