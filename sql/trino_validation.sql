SHOW CATALOGS;
SHOW SCHEMAS FROM iceberg;
SHOW TABLES FROM iceberg.gold;
SELECT * FROM iceberg.gold.daily_sales ORDER BY order_dt, province;
SELECT * FROM iceberg.gold."daily_sales$snapshots";
