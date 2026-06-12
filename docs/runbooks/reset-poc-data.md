# Reset POC Data

Use this when catalog metadata or MinIO objects are inconsistent during experiments.

```bash
make reset
make up
make smoke
```

This command removes Docker Compose volumes and generated local folders. It is safe for POC data, but it destroys all local tables, Superset metadata, Airflow metadata, and Grafana state.
