# Scenario 17: Failure and Recovery Drill

Goal: understand common local failure modes and recovery steps.

Manual drills:

- Stop Trino, run a Trino query, restart Trino, and validate `SHOW CATALOGS`.
- Stop MinIO, run a Spark write, restart MinIO, and validate the baseline again.
- Change the expected quality failure scenario to hard fail, then observe Airflow task behavior.

Pass criteria:

- The failure mode is understandable from logs.
- Recovery commands restore the service.
- The relevant runbook points to the right logs and health checks.

Primary docs:

- `docs/runbooks/troubleshooting.md`
- `docs/runbooks/startup-shutdown.md`

