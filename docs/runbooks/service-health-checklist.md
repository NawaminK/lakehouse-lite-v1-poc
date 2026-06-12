# Service Health Checklist

Use this checklist before running scenarios or debugging a data issue.

| Service | Check | Expected |
|---|---|---|
| MinIO API | `curl http://localhost:9000/minio/health/live` | HTTP 200 |
| MinIO Console | Open `http://localhost:9001` | Login page, `admin/password` works |
| Iceberg REST | `curl http://localhost:8181/v1/config` | JSON response |
| Spark/Jupyter | Open `http://localhost:8888` | Jupyter responds or token prompt appears |
| Trino | `docker compose exec trino trino --server http://localhost:8080 --execute "SHOW CATALOGS"` | `iceberg` catalog appears |
| Superset | Open `http://localhost:8088/health` | Healthy response |
| Airflow | Open `http://localhost:8081` | Login page, `admin/admin` works |
| Prometheus | Open `http://localhost:9090/-/ready` | Ready response |
| Grafana | Open `http://localhost:3000/api/health` | JSON health response |
| cAdvisor | Open `http://localhost:8090` | Container metrics UI appears |

Run the automated readiness script:

```bash
./infra/scripts/wait-for-services.sh
```

Then run:

```bash
make smoke
```

