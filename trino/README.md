# Trino

Trino is the SQL serving layer for the POC.

## Purpose

- Query Iceberg tables with SQL.
- Serve Superset dashboards.
- Serve AI read-only SQL access.
- Inspect Iceberg metadata tables.

## Common commands

```bash
docker compose exec trino trino --server http://localhost:8080 --execute "SHOW CATALOGS"
docker compose exec trino trino --server http://localhost:8080 --execute "SHOW TABLES FROM iceberg.gold"
docker compose exec trino trino --server http://localhost:8080 --execute "SELECT * FROM iceberg.gold.daily_sales"
```

## Key config

- `trino/etc/catalog/iceberg.properties`
