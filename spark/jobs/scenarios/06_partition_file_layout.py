import sys

sys.path.append("/home/iceberg/jobs")
from common import create_spark, ensure_scenarios_namespace, print_header, show_sql

spark = create_spark("scenario-06-partition-file-layout")
ensure_scenarios_namespace(spark)

TABLE = "lakehouse.scenarios.orders_partitioned"

print_header("Scenario 06 - Partitioning and file layout inspection")
print("Goal: prove that an Iceberg table can use hidden partitioning and expose file-level metadata.")

spark.sql(f"DROP TABLE IF EXISTS {TABLE}")
spark.sql(f"""
CREATE TABLE {TABLE} (
  order_id BIGINT,
  customer_id STRING,
  order_ts TIMESTAMP,
  province STRING,
  amount DECIMAL(12,2)
)
USING iceberg
PARTITIONED BY (days(order_ts), province)
""")

spark.sql(f"""
INSERT INTO {TABLE} VALUES
  (2001, 'C200', TIMESTAMP '2026-06-01 08:10:00', 'Bangkok',    100.00),
  (2002, 'C201', TIMESTAMP '2026-06-01 09:20:00', 'Bangkok',    220.00),
  (2003, 'C202', TIMESTAMP '2026-06-02 10:30:00', 'Phuket',      75.00),
  (2004, 'C203', TIMESTAMP '2026-06-02 11:40:00', 'Chiang Mai', 140.00),
  (2005, 'C204', TIMESTAMP '2026-06-03 12:50:00', 'Bangkok',    310.00)
""")

show_sql(spark, f"SELECT * FROM {TABLE} ORDER BY order_ts, order_id", "Partitioned table data")
show_sql(
    spark,
    f"""
    SELECT file_path, partition, record_count, file_size_in_bytes
    FROM {TABLE}.files
    ORDER BY file_path
    """,
    "Iceberg files metadata table",
)

print_header("Query plan for date/province filter")
plan_rows = spark.sql(f"""
EXPLAIN FORMATTED
SELECT order_id, amount
FROM {TABLE}
WHERE order_ts >= TIMESTAMP '2026-06-02 00:00:00'
  AND order_ts <  TIMESTAMP '2026-06-03 00:00:00'
  AND province = 'Phuket'
""").collect()
for row in plan_rows:
    print(row[0])

print("PASS: Scenario 06 completed.")
spark.stop()
