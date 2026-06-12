-- Scenario SQL 03 - Lightweight SQL assertions
-- Result shows PASS for each row when scenarios have run successfully.
-- Any failed assertion raises a Trino error so automation exits non-zero.

WITH checks AS (
  SELECT
    'gold.daily_sales has rows' AS check_name,
    CASE WHEN c > 0 THEN 'PASS' ELSE 'FAIL' END AS result,
    CAST(c AS VARCHAR) AS actual
  FROM (SELECT COUNT(*) c FROM iceberg.gold.daily_sales) AS x

  UNION ALL

  SELECT
    'schema evolution row count = 6' AS check_name,
    CASE WHEN c = 6 THEN 'PASS' ELSE 'FAIL' END AS result,
    CAST(c AS VARCHAR) AS actual
  FROM (SELECT COUNT(*) c FROM iceberg.scenarios.orders_schema_evolution) AS x

  UNION ALL

  SELECT
    'active customers after CDC merge = 3' AS check_name,
    CASE WHEN c = 3 THEN 'PASS' ELSE 'FAIL' END AS result,
    CAST(c AS VARCHAR) AS actual
  FROM (SELECT COUNT(*) c FROM iceberg.scenarios.customers_current WHERE is_deleted = false) AS x

  UNION ALL

  SELECT
    'time travel current table rows = 4' AS check_name,
    CASE WHEN c = 4 THEN 'PASS' ELSE 'FAIL' END AS result,
    CAST(c AS VARCHAR) AS actual
  FROM (SELECT COUNT(*) c FROM iceberg.scenarios.account_balances_history) AS x

  UNION ALL

  SELECT
    'partitioned table rows = 5' AS check_name,
    CASE WHEN c = 5 THEN 'PASS' ELSE 'FAIL' END AS result,
    CAST(c AS VARCHAR) AS actual
  FROM (SELECT COUNT(*) c FROM iceberg.scenarios.orders_partitioned) AS x

  UNION ALL

  SELECT
    'quality bad table rows = 6' AS check_name,
    CASE WHEN c = 6 THEN 'PASS' ELSE 'FAIL' END AS result,
    CAST(c AS VARCHAR) AS actual
  FROM (SELECT COUNT(*) c FROM iceberg.scenarios.orders_quality_bad) AS x

  UNION ALL

  SELECT
    'maintenance demo rows = 10' AS check_name,
    CASE WHEN c = 10 THEN 'PASS' ELSE 'FAIL' END AS result,
    CAST(c AS VARCHAR) AS actual
  FROM (SELECT COUNT(*) c FROM iceberg.scenarios.maintenance_demo) AS x

  UNION ALL

  SELECT
    'backfill gold aggregate rows = 4' AS check_name,
    CASE WHEN c = 4 THEN 'PASS' ELSE 'FAIL' END AS result,
    CAST(c AS VARCHAR) AS actual
  FROM (SELECT COUNT(*) c FROM iceberg.scenarios.daily_sales_backfill) AS x

  UNION ALL

  SELECT
    'backfill total net_sales = 670.00' AS check_name,
    CASE WHEN total_net_sales = DECIMAL '670.00' THEN 'PASS' ELSE 'FAIL' END AS result,
    CAST(total_net_sales AS VARCHAR) AS actual
  FROM (
    SELECT CAST(SUM(net_sales) AS DECIMAL(12,2)) AS total_net_sales
    FROM iceberg.scenarios.daily_sales_backfill
  ) AS x

  UNION ALL

  SELECT
    'backfill Bangkok refund adjusted = 280.00' AS check_name,
    CASE WHEN matched_rows = 1 AND net_sales = DECIMAL '280.00' AND order_count = 3 THEN 'PASS' ELSE 'FAIL' END AS result,
    'rows=' || CAST(matched_rows AS VARCHAR)
      || ', net_sales=' || COALESCE(CAST(net_sales AS VARCHAR), 'NULL')
      || ', orders=' || COALESCE(CAST(order_count AS VARCHAR), 'NULL') AS actual
  FROM (
    SELECT
      COUNT(*) AS matched_rows,
      CAST(MAX(net_sales) AS DECIMAL(12,2)) AS net_sales,
      MAX(order_count) AS order_count
    FROM iceberg.scenarios.daily_sales_backfill
    WHERE order_dt = DATE '2026-06-10' AND province = 'Bangkok'
  ) AS x
),
enforced AS (
  SELECT
    check_name,
    CASE
      WHEN result = 'PASS' THEN result
      ELSE fail('SQL assertion failed: ' || check_name || '; actual=' || COALESCE(actual, 'NULL'))
    END AS result,
    actual
  FROM checks
)
SELECT check_name, result, actual
FROM enforced
ORDER BY check_name;
