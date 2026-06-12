# Superset to Trino Connection Runbook

## Connection string

Use this first:

```text
trino://admin@trino:8080/iceberg
```

Then use schema `gold` in SQL Lab or dataset creation.

Alternative with schema:

```text
trino://admin@trino:8080/iceberg/gold
```

## Why `trino` instead of `localhost`

Superset and Trino run in different Docker containers. From inside the Superset container, `localhost` means the Superset container itself. The Docker Compose service name `trino` resolves to the Trino container.

## Driver check

The Superset image uses `/app/.venv`. Check driver installation in that environment:

```bash
docker compose exec -T superset /app/.venv/bin/python - <<'PY'
import trino
import sqlalchemy_trino
print("OK")
PY
```

## SQL test

```bash
docker compose exec -T superset /app/.venv/bin/python - <<'PY'
from sqlalchemy import create_engine, text
engine = create_engine("trino://admin@trino:8080/iceberg/gold")
with engine.connect() as conn:
    print(conn.execute(text("SHOW TABLES")).fetchall())
PY
```
