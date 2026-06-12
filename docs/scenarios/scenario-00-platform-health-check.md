# Scenario 00: Platform Health Check

Goal: confirm the local Docker Compose platform is ready before testing data behavior.

Run:

```bash
docker compose ps
./infra/scripts/wait-for-services.sh
docker compose exec trino trino --server http://localhost:8080 --execute "SHOW CATALOGS"
```

Pass criteria:

- Core containers are running or healthy.
- MinIO, Iceberg REST, Trino, Superset, Prometheus, Grafana, and cAdvisor respond.
- Trino shows at least `iceberg` and `system` catalogs.

Primary docs:

- `docs/runbooks/startup-shutdown.md`
- `docs/runbooks/troubleshooting.md`

