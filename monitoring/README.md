# Monitoring

The POC uses cAdvisor, Prometheus, and Grafana.

## Flow

```text
Docker containers -> cAdvisor -> Prometheus -> Grafana
```

## URLs

- cAdvisor: http://localhost:8090
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Grafana default credential: `admin` / `admin`

## Example PromQL

```promql
up
container_memory_usage_bytes{name!=""}
rate(container_cpu_usage_seconds_total{name!=""}[5m])
rate(container_network_receive_bytes_total{name!=""}[5m])
```

## Starter dashboard

Import this file into Grafana after adding Prometheus as a data source:

```text
monitoring/grafana/container-dashboard-v1.json
```
