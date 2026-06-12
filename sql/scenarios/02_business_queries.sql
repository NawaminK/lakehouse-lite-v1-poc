-- Scenario SQL 02 - Business-facing queries through Trino
-- These queries emulate analyst/BI access through the SQL serving layer.

SELECT
  order_dt,
  province,
  net_sales,
  order_count
FROM iceberg.gold.daily_sales
ORDER BY order_dt, province;

SELECT
  province,
  SUM(net_sales) AS total_net_sales,
  SUM(order_count) AS total_orders
FROM iceberg.gold.daily_sales
GROUP BY province
ORDER BY total_net_sales DESC;

SELECT
  order_dt,
  SUM(net_sales) AS total_net_sales
FROM iceberg.scenarios.daily_sales_backfill
GROUP BY order_dt
ORDER BY order_dt;

SELECT
  tier,
  COUNT(*) AS active_customers
FROM iceberg.scenarios.customers_current
WHERE is_deleted = false
GROUP BY tier
ORDER BY tier;
