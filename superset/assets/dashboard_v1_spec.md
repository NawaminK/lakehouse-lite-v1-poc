# Lakehouse POC Dashboard v1 Spec

## Data source

Connection:

```text
trino://admin@trino:8080/iceberg
```

Dataset:

```text
schema: gold
table: daily_sales
```

## Metrics

| Metric | Expression | Purpose |
|---|---|---|
| `total_net_sales` | `SUM(net_sales)` | Revenue after refunds |
| `total_orders` | `SUM(order_count)` | Total order records in aggregate |
| `avg_net_sales_per_order` | `SUM(net_sales) / NULLIF(SUM(order_count), 0)` | Simple productivity metric |

## Charts

| Chart | Visualization | Dimensions | Metrics |
|---|---|---|---|
| Net sales by province | Bar chart | `province` | `total_net_sales` |
| Orders by province | Bar chart | `province` | `total_orders` |
| Daily net sales | Time-series line or table | `order_dt` | `total_net_sales` |
| Daily sales detail | Table | `order_dt`, `province` | `net_sales`, `order_count` |

## Validation checklist

- Superset database connection uses service name `trino`, not `localhost`.
- Dataset columns appear for `daily_sales`.
- Each chart refreshes without query errors.
- Dashboard screenshot or query output is attached to the PR.

