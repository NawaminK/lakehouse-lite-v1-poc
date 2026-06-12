import sys
from decimal import Decimal

sys.path.append("/home/iceberg/jobs")
from common import create_spark, ensure_scenarios_namespace, print_header, show_sql

spark = create_spark("scenario-09-late-arriving-backfill")
ensure_scenarios_namespace(spark)

BRONZE = "lakehouse.scenarios.orders_backfill_raw"
GOLD = "lakehouse.scenarios.daily_sales_backfill"

print_header("Scenario 09 - Late arriving data and gold table rebuild")
print("Goal: prove that a pipeline can incorporate late data and rebuild a business aggregate deterministically.")

spark.sql(f"DROP TABLE IF EXISTS {GOLD}")
spark.sql(f"DROP TABLE IF EXISTS {BRONZE}")

spark.sql(f"""
CREATE TABLE {BRONZE} (
  order_id BIGINT,
  order_dt DATE,
  province STRING,
  amount DECIMAL(12,2),
  status STRING,
  load_batch STRING
)
USING iceberg
""")

spark.sql(f"""
INSERT INTO {BRONZE} VALUES
  (4001, DATE '2026-06-10', 'Bangkok', 100.00, 'paid', 'initial'),
  (4002, DATE '2026-06-10', 'Bangkok', 200.00, 'paid', 'initial'),
  (4003, DATE '2026-06-10', 'Phuket',   50.00, 'paid', 'initial')
""")

spark.sql(f"""
CREATE TABLE {GOLD}
USING iceberg
AS
SELECT
  order_dt,
  province,
  SUM(CASE WHEN status = 'paid' THEN amount ELSE -amount END) AS net_sales,
  COUNT(*) AS order_count,
  MAX(load_batch) AS last_rebuild_source_batch
FROM {BRONZE}
GROUP BY order_dt, province
""")

show_sql(spark, f"SELECT * FROM {GOLD} ORDER BY order_dt, province", "Gold table after initial load")

print_header("Append late-arriving records")
spark.sql(f"""
INSERT INTO {BRONZE} VALUES
  (3998, DATE '2026-06-09', 'Bangkok', 300.00, 'paid',   'late_batch_01'),
  (3999, DATE '2026-06-09', 'Phuket',   40.00, 'paid',   'late_batch_01'),
  (4002, DATE '2026-06-10', 'Bangkok',  20.00, 'refund', 'late_batch_01')
""")

show_sql(spark, f"SELECT * FROM {BRONZE} ORDER BY order_dt, order_id, status", "Bronze table after late batch")

spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD}
USING iceberg
AS
SELECT
  order_dt,
  province,
  SUM(CASE WHEN status = 'paid' THEN amount ELSE -amount END) AS net_sales,
  COUNT(*) AS order_count,
  MAX(load_batch) AS last_rebuild_source_batch
FROM {BRONZE}
GROUP BY order_dt, province
""")

show_sql(spark, f"SELECT * FROM {GOLD} ORDER BY order_dt, province", "Gold table after deterministic rebuild")
show_sql(spark, f"SELECT snapshot_id, committed_at, operation FROM {GOLD}.snapshots ORDER BY committed_at", "Gold table snapshots")

summary = spark.sql(f"""
SELECT
  COUNT(*) AS row_count,
  CAST(SUM(net_sales) AS DECIMAL(12,2)) AS total_net_sales,
  SUM(order_count) AS total_order_count
FROM {GOLD}
""").collect()[0]

if summary["row_count"] != 4:
    raise RuntimeError(f"Expected 4 aggregate rows after backfill rebuild, got {summary['row_count']}")

if summary["total_net_sales"] != Decimal("670.00"):
    raise RuntimeError(f"Expected total net_sales 670.00 after backfill rebuild, got {summary['total_net_sales']}")

if int(summary["total_order_count"]) != 6:
    raise RuntimeError(f"Expected total order_count 6 after backfill rebuild, got {summary['total_order_count']}")

bangkok_20260610 = spark.sql(f"""
SELECT CAST(net_sales AS DECIMAL(12,2)) AS net_sales, order_count
FROM {GOLD}
WHERE order_dt = DATE '2026-06-10' AND province = 'Bangkok'
""").collect()[0]

if bangkok_20260610["net_sales"] != Decimal("280.00") or int(bangkok_20260610["order_count"]) != 3:
    raise RuntimeError(
        "Expected Bangkok 2026-06-10 to have net_sales 280.00 and order_count 3 "
        f"after refund adjustment, got net_sales={bangkok_20260610['net_sales']}, "
        f"order_count={bangkok_20260610['order_count']}"
    )

print("PASS: Scenario 09 completed.")
spark.stop()
