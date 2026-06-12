from typing import Optional

from pyspark.sql import SparkSession


def create_spark(app_name: str) -> SparkSession:
    """Create a SparkSession configured for the local POC Iceberg REST catalog."""
    return (
        SparkSession.builder
        .appName(app_name)
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .config("spark.sql.catalog.lakehouse", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.lakehouse.type", "rest")
        .config("spark.sql.catalog.lakehouse.uri", "http://iceberg-rest:8181")
        .config("spark.sql.catalog.lakehouse.warehouse", "s3://warehouse/")
        .config("spark.sql.catalog.lakehouse.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")
        .config("spark.sql.catalog.lakehouse.s3.endpoint", "http://minio:9000")
        .config("spark.sql.catalog.lakehouse.s3.path-style-access", "true")
        .config("spark.sql.defaultCatalog", "lakehouse")
        .getOrCreate()
    )


def ensure_scenarios_namespace(spark: SparkSession) -> None:
    spark.sql("CREATE NAMESPACE IF NOT EXISTS lakehouse.scenarios")


def ensure_core_namespaces(spark: SparkSession) -> None:
    for namespace in ["bronze", "silver", "gold"]:
        spark.sql(f"CREATE NAMESPACE IF NOT EXISTS lakehouse.{namespace}")


def print_header(title: str) -> None:
    line = "=" * 100
    print(f"\n{line}\n{title}\n{line}")


def show_sql(spark: SparkSession, sql_text: str, title: Optional[str] = None, rows: int = 50) -> None:
    if title:
        print_header(title)
    print(sql_text.strip())
    spark.sql(sql_text).show(rows, truncate=False)
