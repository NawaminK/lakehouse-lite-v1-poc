# Scenario 16: Observability Smoke Test

Goal: confirm container health and resource usage are visible.

Manual steps:

1. Open Prometheus at `http://localhost:9090`.
2. Query `up`.
3. Query `container_memory_usage_bytes{name!=""}`.
4. Open Grafana at `http://localhost:3000`.
5. Add Prometheus data source `http://prometheus:9090`.

Pass criteria:

- Prometheus can scrape cAdvisor.
- Grafana can query Prometheus.
- CPU, memory, network, and filesystem signals are available.

Dashboard artifact:

- `monitoring/grafana/container-dashboard-v1.json`

