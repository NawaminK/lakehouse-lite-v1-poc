# Observability Learning Path

## Goal

Understand service health and resource usage during Spark, Trino, Superset, and MinIO activity.

## Concepts

- cAdvisor container metrics.
- Prometheus scrape targets.
- PromQL.
- Grafana dashboards.

## Hands-on tasks

- Open cAdvisor at http://localhost:8090.
- Open Prometheus at http://localhost:9090.
- Query `up`.
- Query container memory usage.
- Add Prometheus as a Grafana data source.
- Build a dashboard for CPU and memory by container.

## Example PromQL

```promql
up
container_memory_usage_bytes{name!=""}
rate(container_cpu_usage_seconds_total{name!=""}[5m])
rate(container_network_receive_bytes_total{name!=""}[5m])
```
