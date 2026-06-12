# Superset Learning Path

## Goal

Create BI datasets, metrics, charts, and dashboards from Trino tables.

## Concepts

- Database connection.
- SQL Lab.
- Dataset.
- Metric.
- Chart.
- Dashboard.
- Native filter.

## Hands-on tasks

1. Connect Superset to Trino using `trino://admin@trino:8080/iceberg`.
2. Query `iceberg.gold.daily_sales` in SQL Lab.
3. Create a dataset from schema `gold`, table `daily_sales`.
4. Create metrics: `SUM(net_sales)`, `SUM(order_count)`.
5. Create a bar chart by province.
6. Create a daily trend chart.
7. Add charts to a dashboard.

## Key files

- `superset/Dockerfile`
- `docs/runbooks/superset-trino-connection.md`
