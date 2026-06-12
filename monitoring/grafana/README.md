# Grafana Assets

Grafana uses Prometheus as its data source in this POC.

## Files

| File | Purpose |
|---|---|
| `container-dashboard-v1.json` | Starter dashboard JSON for cAdvisor container metrics |

## Data source

Inside Grafana, add Prometheus with this URL:

```text
http://prometheus:9090
```

If your Grafana data source UID is not `prometheus`, update the dashboard JSON after import.

