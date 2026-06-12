#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

./infra/scripts/wait-for-services.sh

echo "Running Spark baseline table creation"
docker compose exec -T spark-iceberg spark-submit /home/iceberg/jobs/01_create_tables.py

echo "Running Spark baseline quality check"
docker compose exec -T spark-iceberg spark-submit /home/iceberg/jobs/02_quality_check.py

echo "Running Trino validation"
docker compose exec -T trino trino --server http://localhost:8080 --file /tmp/sql/trino_validation.sql

echo "Checking table visibility"
docker compose exec -T trino trino --server http://localhost:8080 --execute "SHOW TABLES FROM iceberg.gold"

echo "Smoke test completed successfully"
