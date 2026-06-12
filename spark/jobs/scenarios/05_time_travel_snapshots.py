import sys

sys.path.append("/home/iceberg/jobs")
from common import create_spark, ensure_scenarios_namespace, print_header, show_sql

spark = create_spark("scenario-05-time-travel-snapshots")
ensure_scenarios_namespace(spark)

TABLE = "lakehouse.scenarios.account_balances_history"

print_header("Scenario 05 - Iceberg snapshots and time travel")
print("Goal: prove that old table versions can be queried through Iceberg snapshot IDs.")

spark.sql(f"DROP TABLE IF EXISTS {TABLE}")
spark.sql(f"""
CREATE TABLE {TABLE} (
  account_id STRING,
  balance DECIMAL(12,2),
  as_of_dt DATE
)
USING iceberg
""")

spark.sql(f"""
INSERT INTO {TABLE} VALUES
  ('A001', 1000.00, DATE '2026-06-01'),
  ('A002', 2500.00, DATE '2026-06-01')
""")

snapshot_v1 = spark.sql(
    f"SELECT snapshot_id FROM {TABLE}.snapshots ORDER BY committed_at DESC LIMIT 1"
).collect()[0]["snapshot_id"]

spark.sql(f"""
INSERT INTO {TABLE} VALUES
  ('A001', 1200.00, DATE '2026-06-02'),
  ('A003',  300.00, DATE '2026-06-02')
""")

snapshot_v2 = spark.sql(
    f"SELECT snapshot_id FROM {TABLE}.snapshots ORDER BY committed_at DESC LIMIT 1"
).collect()[0]["snapshot_id"]

show_sql(spark, f"SELECT * FROM {TABLE} ORDER BY account_id, as_of_dt", "Current table version")
show_sql(spark, f"SELECT snapshot_id, committed_at, operation FROM {TABLE}.snapshots ORDER BY committed_at", "Snapshot timeline")

print_header("Read table as of the first snapshot")
print(f"snapshot_v1 = {snapshot_v1}")
print(f"snapshot_v2 = {snapshot_v2}")

v1_df = (
    spark.read
    .format("iceberg")
    .option("snapshot-id", str(snapshot_v1))
    .load(TABLE)
)
v1_df.orderBy("account_id", "as_of_dt").show(truncate=False)

current_count = spark.table(TABLE).count()
v1_count = v1_df.count()
if current_count != 4 or v1_count != 2:
    raise RuntimeError(f"Unexpected counts. current={current_count}, v1={v1_count}")

print("PASS: Scenario 05 completed.")
spark.stop()
