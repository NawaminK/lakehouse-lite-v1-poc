#!/usr/bin/env bash
set -euo pipefail

wait_http() {
  local name="$1"
  local url="$2"
  local max_attempts="${3:-60}"
  local attempt=1

  echo "Waiting for ${name}: ${url}"
  until curl -fsS "$url" >/dev/null 2>&1; do
    if [ "$attempt" -ge "$max_attempts" ]; then
      echo "ERROR: ${name} did not become ready after ${max_attempts} attempts" >&2
      exit 1
    fi
    attempt=$((attempt + 1))
    sleep 2
  done
  echo "OK: ${name} is ready"
}

wait_http "MinIO" "http://localhost:9000/minio/health/live" 60
wait_http "Iceberg REST" "http://localhost:8181/v1/config" 60
wait_http "Trino" "http://localhost:8080/v1/info" 60
wait_http "Superset" "http://localhost:8088/health" 90 || true
wait_http "Prometheus" "http://localhost:9090/-/ready" 60
wait_http "Grafana" "http://localhost:3000/api/health" 60
