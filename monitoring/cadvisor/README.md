# cAdvisor

cAdvisor exports container resource metrics for Prometheus.

## URL

```text
http://localhost:8090
```

## Useful metrics

```promql
container_cpu_usage_seconds_total{name!=""}
container_memory_usage_bytes{name!=""}
container_network_receive_bytes_total{name!=""}
container_network_transmit_bytes_total{name!=""}
container_fs_usage_bytes{name!=""}
```

Use `monitoring/grafana/container-dashboard-v1.json` as the first Grafana dashboard.

