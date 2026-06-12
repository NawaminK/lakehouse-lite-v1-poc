# Superset

Superset is the BI and dashboard layer.

## URL

http://localhost:8088

Default user: `admin`
Default password: `admin`

## Trino connection URI

Use this first:

```text
trino://admin@trino:8080/iceberg
```

Then select schema `gold` in SQL Lab or dataset creation.

## Recommended first dataset

- Database: Trino
- Schema: gold
- Table: daily_sales

## Recommended first metrics

- `total_net_sales`: `SUM(net_sales)`
- `total_orders`: `SUM(order_count)`

## Dashboard v1 spec

See:

```text
superset/assets/dashboard_v1_spec.md
```
