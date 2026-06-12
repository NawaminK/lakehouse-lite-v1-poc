import sys
from pathlib import Path

from pyspark.sql.functions import col, current_timestamp, date_format, to_date

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import create_spark, print_header

SOURCE_PATH = "/home/iceberg/sample-data/csv/orders.csv"
BRONZE = "lakehouse.scenarios.template_orders_raw"
SILVER = "lakehouse.scenarios.template_orders_clean"
REJECTED = "lakehouse.scenarios.template_orders_rejected"
GOLD = "lakehouse.scenarios.template_daily_sales"

spark = create_spark("template-csv-to-bronze-silver-gold")
spark.sql("CREATE NAMESPACE IF NOT EXISTS lakehouse.scenarios")

print_header("Read CSV source")
source_df = spark.read.option("header", "true").csv(SOURCE_PATH)

bronze_df = (
    source_df
    .withColumn("ingested_at", current_timestamp())
)

bronze_df.writeTo(BRONZE).using("iceberg").createOrReplace()

typed_df = (
    bronze_df
    .select(
        col("order_id").cast("bigint").alias("order_id"),
        col("customer_id"),
        to_date(col("order_date")).alias("order_dt"),
        col("province"),
        col("amount").cast("decimal(12,2)").alias("amount"),
        col("status"),
        col("ingested_at"),
    )
    .withColumn("yyyymm", date_format(col("order_dt"), "yyyyMM"))
)

valid_df = typed_df.filter(
    col("order_id").isNotNull()
    & col("customer_id").isNotNull()
    & col("order_dt").isNotNull()
    & col("amount").isNotNull()
    & (col("amount") >= 0)
    & col("status").isin("paid", "refund")
)

rejected_df = typed_df.subtract(valid_df)

valid_df.writeTo(SILVER).using("iceberg").createOrReplace()
rejected_df.writeTo(REJECTED).using("iceberg").createOrReplace()

spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD}
USING iceberg
AS
SELECT
  order_dt,
  province,
  SUM(CASE WHEN status = 'paid' THEN amount ELSE -amount END) AS net_sales,
  COUNT(*) AS order_count
FROM {SILVER}
GROUP BY order_dt, province
""")

print_header("Template output tables")
for table_name in [BRONZE, SILVER, REJECTED, GOLD]:
    print(table_name)
    spark.table(table_name).show(truncate=False)

spark.stop()

