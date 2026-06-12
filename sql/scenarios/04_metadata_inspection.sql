-- Scenario SQL 04 - Iceberg metadata table inspection through Trino
-- Useful for explaining snapshots, history, and physical file layout.

SELECT snapshot_id, committed_at, operation, summary
FROM iceberg.gold."daily_sales$snapshots"
ORDER BY committed_at;

SELECT snapshot_id, made_current_at, parent_id, is_current_ancestor
FROM iceberg.scenarios."orders_schema_evolution$history"
ORDER BY made_current_at;

SELECT snapshot_id, committed_at, operation
FROM iceberg.scenarios."customers_current$snapshots"
ORDER BY committed_at;

SELECT file_path, record_count, file_size_in_bytes
FROM iceberg.scenarios."orders_partitioned$files"
ORDER BY file_path;

SELECT snapshot_id, committed_at, operation
FROM iceberg.scenarios."daily_sales_backfill$snapshots"
ORDER BY committed_at;
