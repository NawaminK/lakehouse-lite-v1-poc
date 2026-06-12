import sys
from pathlib import Path

from pyspark.sql.functions import col

sys.path.append(str(Path(__file__).resolve().parent))
from common import create_spark

spark = create_spark("lakehouse-lite-v1-quality-check")

checks = []
orders = spark.table("lakehouse.silver.orders_clean")

def check(name, condition, detail):
    if condition:
        print(f"PASS: {name}")
    else:
        print(f"FAIL: {name} - {detail}")
        checks.append((name, detail))

check(
    "silver.orders_clean has rows",
    orders.count() > 0,
    "table is empty",
)

check(
    "order_id is not null",
    orders.filter(col("order_id").isNull()).count() == 0,
    "order_id contains nulls",
)

check(
    "amount is non-negative in raw order records",
    orders.filter(col("amount") < 0).count() == 0,
    "amount contains negative values",
)

check(
    "status is allowed",
    orders.filter(~col("status").isin("paid", "refund")).count() == 0,
    "status contains values outside paid/refund",
)

if checks:
    raise RuntimeError(f"Data quality failed: {checks}")

spark.stop()
