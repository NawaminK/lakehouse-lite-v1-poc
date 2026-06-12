import sys
from pathlib import Path

from pyspark.sql.functions import col, current_timestamp, date_format, to_date

sys.path.append(str(Path(__file__).resolve().parent))
from common import create_spark, ensure_core_namespaces, print_header

SOURCE_PATH = "/home/iceberg/sample-data/csv/orders.csv"

spark = create_spark("lakehouse-lite-v1-create-tables")
ensure_core_namespaces(spark)

print_header("Read sample CSV source")
print(f"source_path = {SOURCE_PATH}")

source_df = spark.read.option("header", "true").csv(SOURCE_PATH)
raw_df = (
    source_df
    .select(
        col("order_id").cast("bigint").alias("order_id"),
        col("customer_id"),
        col("order_date"),
        col("province"),
        col("amount").cast("decimal(12,2)").alias("amount"),
        col("status"),
    )
    .withColumn("ingested_at", current_timestamp())
)

raw_df.writeTo("lakehouse.bronze.orders_raw").using("iceberg").createOrReplace()

clean_df = (
    raw_df
    .withColumn("order_dt", to_date(col("order_date")))
    .withColumn("yyyymm", date_format(col("order_dt"), "yyyyMM"))
    .filter(col("amount").isNotNull())
)

clean_df.writeTo("lakehouse.silver.orders_clean").using("iceberg").createOrReplace()

spark.sql("""
CREATE OR REPLACE TABLE lakehouse.gold.daily_sales
USING iceberg
AS
SELECT
  order_dt,
  province,
  SUM(CASE WHEN status = 'paid' THEN amount ELSE -amount END) AS net_sales,
  COUNT(*) AS order_count
FROM lakehouse.silver.orders_clean
GROUP BY order_dt, province
""")

print("Created Iceberg tables:")
spark.sql("SHOW TABLES IN lakehouse.bronze").show(truncate=False)
spark.sql("SHOW TABLES IN lakehouse.silver").show(truncate=False)
spark.sql("SHOW TABLES IN lakehouse.gold").show(truncate=False)
spark.sql("SELECT * FROM lakehouse.gold.daily_sales ORDER BY order_dt, province").show(truncate=False)

spark.stop()
