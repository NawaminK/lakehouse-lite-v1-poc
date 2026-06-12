import sys

sys.path.append("/home/iceberg/jobs")
from common import create_spark, ensure_scenarios_namespace, print_header, show_sql

spark = create_spark("scenario-03-schema-evolution")
ensure_scenarios_namespace(spark)

TABLE = "lakehouse.scenarios.orders_schema_evolution"

print_header("Scenario 03 - Schema evolution")
print("Goal: prove that an Iceberg table can evolve schema without rewriting old data files.")

spark.sql(f"DROP TABLE IF EXISTS {TABLE}")

spark.sql(f"""
CREATE TABLE {TABLE} (
  order_id BIGINT,
  customer_id STRING,
  order_dt DATE,
  amount DECIMAL(12,2),
  status STRING
)
USING iceberg
""")

spark.sql(f"""
INSERT INTO {TABLE} VALUES
  (1001, 'C100', DATE '2026-06-04', 100.00, 'paid'),
  (1002, 'C101', DATE '2026-06-04', 250.00, 'paid'),
  (1003, 'C102', DATE '2026-06-05',  50.00, 'refund')
""")

show_sql(spark, f"SELECT * FROM {TABLE} ORDER BY order_id", "Before schema evolution")
print_header("Schema before ALTER TABLE")
spark.table(TABLE).printSchema()

spark.sql(f"""
ALTER TABLE {TABLE}
ADD COLUMNS (
  coupon_code STRING,
  channel STRING
)
""")

spark.sql(f"""
INSERT INTO {TABLE}
  (order_id, customer_id, order_dt, amount, status, coupon_code, channel)
VALUES
  (1004, 'C103', DATE '2026-06-06',  80.00, 'paid',   'WELCOME10', 'mobile'),
  (1005, 'C104', DATE '2026-06-06', 125.00, 'paid',   NULL,        'web'),
  (1006, 'C101', DATE '2026-06-07',  30.00, 'refund', 'WELCOME10', 'mobile')
""")

print_header("Schema after ALTER TABLE")
spark.table(TABLE).printSchema()
show_sql(spark, f"SELECT * FROM {TABLE} ORDER BY order_id", "After schema evolution")
show_sql(
    spark,
    f"""
    SELECT order_id, coupon_code, channel
    FROM {TABLE}
    ORDER BY order_id
    """,
    "Old rows keep NULL values for newly added columns",
)
show_sql(
    spark,
    f"SELECT snapshot_id, committed_at, operation FROM {TABLE}.snapshots ORDER BY committed_at",
    "Iceberg snapshots created by create/insert/schema evolution/append operations",
)

print("PASS: Scenario 03 completed.")
spark.stop()
