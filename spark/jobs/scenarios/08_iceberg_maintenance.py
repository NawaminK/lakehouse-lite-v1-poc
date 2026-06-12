import sys

sys.path.append("/home/iceberg/jobs")
from common import create_spark, ensure_scenarios_namespace, print_header, show_sql

spark = create_spark("scenario-08-iceberg-maintenance")
ensure_scenarios_namespace(spark)

TABLE = "lakehouse.scenarios.maintenance_demo"

print_header("Scenario 08 - Iceberg metadata and maintenance procedures")
print("Goal: show why snapshot/file maintenance matters and demonstrate the expire_snapshots procedure when available.")

spark.sql(f"DROP TABLE IF EXISTS {TABLE}")
spark.sql(f"""
CREATE TABLE {TABLE} (
  id BIGINT,
  batch_id INT,
  payload STRING
)
USING iceberg
""")

for batch_id in range(1, 6):
    spark.sql(f"""
    INSERT INTO {TABLE} VALUES
      ({batch_id * 10 + 1}, {batch_id}, 'event-{batch_id}-a'),
      ({batch_id * 10 + 2}, {batch_id}, 'event-{batch_id}-b')
    """)

show_sql(spark, f"SELECT * FROM {TABLE} ORDER BY batch_id, id", "Rows after several small appends")
show_sql(spark, f"SELECT COUNT(*) AS snapshot_count FROM {TABLE}.snapshots", "Snapshot count before maintenance")
show_sql(spark, f"SELECT COUNT(*) AS data_file_count FROM {TABLE}.files", "Data file count before maintenance")
show_sql(spark, f"SELECT snapshot_id, committed_at, operation FROM {TABLE}.snapshots ORDER BY committed_at", "Snapshots before maintenance")

print_header("Attempt expire_snapshots")
try:
    spark.sql("""
    CALL lakehouse.system.expire_snapshots(
      table => 'scenarios.maintenance_demo',
      older_than => TIMESTAMP '2099-01-01 00:00:00',
      retain_last => 1
    )
    """).show(truncate=False)
    print("Maintenance procedure executed successfully.")
except Exception as exc:
    print("Maintenance procedure could not be executed in this local image/version.")
    print("This does not invalidate the scenario; use the printed SQL as the production maintenance pattern.")
    print(f"Reason: {exc}")

show_sql(spark, f"SELECT COUNT(*) AS snapshot_count FROM {TABLE}.snapshots", "Snapshot count after maintenance attempt")
show_sql(spark, f"SELECT COUNT(*) AS data_file_count FROM {TABLE}.files", "Data file count after maintenance attempt")

print("PASS: Scenario 08 completed.")
spark.stop()
