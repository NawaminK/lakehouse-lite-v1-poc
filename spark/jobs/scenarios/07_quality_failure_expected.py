import sys

from pyspark.sql.functions import col, count as spark_count
from pyspark.sql.types import DateType, DecimalType, LongType, StringType, StructField, StructType

sys.path.append("/home/iceberg/jobs")
from common import create_spark, ensure_scenarios_namespace, print_header, show_sql

spark = create_spark("scenario-07-quality-failure-expected")
ensure_scenarios_namespace(spark)

TABLE = "lakehouse.scenarios.orders_quality_bad"

print_header("Scenario 07 - Expected data quality failure")
print("Goal: prove that the platform can detect bad records. This scenario exits successfully only when violations are detected.")

spark.sql(f"DROP TABLE IF EXISTS {TABLE}")

schema = StructType([
    StructField("order_id", LongType(), True),
    StructField("customer_id", StringType(), True),
    StructField("order_dt", DateType(), True),
    StructField("province", StringType(), True),
    StructField("amount", DecimalType(12, 2), True),
    StructField("status", StringType(), True),
])

rows = [
    (3001, "C300", "2026-06-01", "Bangkok", "100.00", "paid"),
    (3001, "C300", "2026-06-01", "Bangkok", "100.00", "paid"),  # duplicate business key
    (None, "C301", "2026-06-01", "Phuket", "50.00", "paid"),      # null key
    (3002, None, "2026-06-02", "Bangkok", "40.00", "paid"),        # missing customer
    (3003, "C303", "2026-06-02", "Bangkok", "-10.00", "paid"),     # invalid amount
    (3004, "C304", "2026-06-02", "Bangkok", "25.00", "void"),      # invalid status
]

# Create with SQL to avoid Python Decimal/date conversion noise in a POC script.
spark.sql(f"""
CREATE TABLE {TABLE} (
  order_id BIGINT,
  customer_id STRING,
  order_dt DATE,
  province STRING,
  amount DECIMAL(12,2),
  status STRING
)
USING iceberg
""")

spark.sql(f"""
INSERT INTO {TABLE} VALUES
  (3001, 'C300', DATE '2026-06-01', 'Bangkok', 100.00, 'paid'),
  (3001, 'C300', DATE '2026-06-01', 'Bangkok', 100.00, 'paid'),
  (NULL, 'C301', DATE '2026-06-01', 'Phuket',   50.00, 'paid'),
  (3002, NULL,   DATE '2026-06-02', 'Bangkok',  40.00, 'paid'),
  (3003, 'C303', DATE '2026-06-02', 'Bangkok', -10.00, 'paid'),
  (3004, 'C304', DATE '2026-06-02', 'Bangkok',  25.00, 'void')
""")

show_sql(spark, f"SELECT * FROM {TABLE} ORDER BY order_id NULLS FIRST", "Bad input records")

df = spark.table(TABLE)
duplicate_key_count = (
    df.groupBy("order_id")
    .agg(spark_count("*").alias("row_count"))
    .filter(col("order_id").isNotNull() & (col("row_count") > 1))
    .count()
)

violations = {
    "null_order_id": df.filter(col("order_id").isNull()).count(),
    "null_customer_id": df.filter(col("customer_id").isNull()).count(),
    "negative_amount": df.filter(col("amount") < 0).count(),
    "invalid_status": df.filter(~col("status").isin("paid", "refund")).count(),
    "duplicate_order_id_groups": duplicate_key_count,
}

print_header("Violation counts")
for name, value in violations.items():
    print(f"{name}: {value}")

expected_nonzero = [
    "null_order_id",
    "null_customer_id",
    "negative_amount",
    "invalid_status",
    "duplicate_order_id_groups",
]
missing = [name for name in expected_nonzero if violations[name] == 0]
if missing:
    raise RuntimeError(f"Expected violations were not detected: {missing}")

print("PASS: Scenario 07 completed. Quality gate detected the expected bad records.")
spark.stop()
