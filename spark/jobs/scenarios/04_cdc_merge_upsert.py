import sys

sys.path.append("/home/iceberg/jobs")
from common import create_spark, ensure_scenarios_namespace, print_header, show_sql

spark = create_spark("scenario-04-cdc-merge-upsert")
ensure_scenarios_namespace(spark)

TABLE = "lakehouse.scenarios.customers_current"

print_header("Scenario 04 - CDC style merge/upsert")
print("Goal: prove that Spark can apply insert/update/delete events into an Iceberg target table using MERGE INTO.")

spark.sql(f"DROP TABLE IF EXISTS {TABLE}")
spark.sql(f"""
CREATE TABLE {TABLE} (
  customer_id STRING,
  full_name STRING,
  tier STRING,
  province STRING,
  updated_at TIMESTAMP,
  is_deleted BOOLEAN
)
USING iceberg
""")

spark.sql(f"""
INSERT INTO {TABLE} VALUES
  ('C001', 'Anan Wong',   'silver', 'Bangkok',    TIMESTAMP '2026-06-01 09:00:00', false),
  ('C002', 'Boon Mee',    'bronze', 'Chiang Mai', TIMESTAMP '2026-06-01 09:00:00', false),
  ('C003', 'Chai Supha',  'gold',   'Phuket',     TIMESTAMP '2026-06-01 09:00:00', false)
""")

show_sql(spark, f"SELECT * FROM {TABLE} ORDER BY customer_id", "Initial current-state table")

spark.sql("""
CREATE OR REPLACE TEMP VIEW customer_changes AS
SELECT * FROM VALUES
  ('C001', 'Anan Wong',      'gold',   'Bangkok',    'U', TIMESTAMP '2026-06-10 10:00:00'),
  ('C004', 'Dao Charoen',    'silver', 'Khon Kaen',  'I', TIMESTAMP '2026-06-10 10:01:00'),
  ('C002', 'Boon Mee',       'bronze', 'Chiang Mai', 'D', TIMESTAMP '2026-06-10 10:02:00'),
  ('C003', 'Chai Suphapong', 'gold',   'Phuket',     'U', TIMESTAMP '2026-06-10 10:03:00')
AS customer_changes(customer_id, full_name, tier, province, operation, change_ts)
""")

show_sql(spark, "SELECT * FROM customer_changes ORDER BY change_ts", "Incoming CDC events")

spark.sql(f"""
MERGE INTO {TABLE} AS t
USING customer_changes AS s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.operation = 'D' THEN UPDATE SET
  full_name = s.full_name,
  tier = s.tier,
  province = s.province,
  updated_at = s.change_ts,
  is_deleted = true
WHEN MATCHED AND s.operation IN ('U', 'I') THEN UPDATE SET
  full_name = s.full_name,
  tier = s.tier,
  province = s.province,
  updated_at = s.change_ts,
  is_deleted = false
WHEN NOT MATCHED AND s.operation IN ('U', 'I') THEN INSERT (
  customer_id,
  full_name,
  tier,
  province,
  updated_at,
  is_deleted
) VALUES (
  s.customer_id,
  s.full_name,
  s.tier,
  s.province,
  s.change_ts,
  false
)
""")

show_sql(spark, f"SELECT * FROM {TABLE} ORDER BY customer_id", "Current-state table after MERGE")
show_sql(spark, f"SELECT snapshot_id, committed_at, operation FROM {TABLE}.snapshots ORDER BY committed_at", "Snapshots after CDC merge")

active_count = spark.sql(f"SELECT COUNT(*) AS c FROM {TABLE} WHERE is_deleted = false").collect()[0]["c"]
if active_count != 3:
    raise RuntimeError(f"Expected 3 active customers after CDC merge, got {active_count}")

print("PASS: Scenario 04 completed.")
spark.stop()
