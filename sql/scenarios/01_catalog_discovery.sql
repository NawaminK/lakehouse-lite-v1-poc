-- Scenario SQL 01 - Catalog discovery
-- Run after the Spark scenarios have created tables.

SHOW CATALOGS;
SHOW SCHEMAS FROM iceberg;
SHOW TABLES FROM iceberg.gold;
SHOW TABLES FROM iceberg.scenarios;
SHOW COLUMNS FROM iceberg.gold.daily_sales;
SHOW COLUMNS FROM iceberg.scenarios.orders_schema_evolution;
