# Contributing

This POC is designed as a team learning project. Keep changes small, documented, and easy to verify.

## First-time setup

```bash
cp .env.example .env
export AIRFLOW_UID=$(id -u)
export DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)
make up
make smoke
```

If `make smoke` fails, check `docs/runbooks/troubleshooting.md` before changing code.

## Branches

Use short-lived branches:

```text
feature/<team>/<short-description>
bugfix/<team>/<short-description>
experiment/<team>/<short-description>
```

Examples:

```text
feature/data/csv-ingestion-template
feature/bi/dashboard-v1
bugfix/platform/trino-catalog-config
```

## Before opening a PR

Run the narrowest useful test plus the baseline smoke test when practical:

```bash
make smoke
make scenarios
python -m unittest discover -s ai-assistant/tests
```

For documentation-only changes, explain why runtime validation was not needed.

## Pull request expectations

Every PR should include:

- Objective and changed areas.
- Test command and result.
- Screenshot or log evidence for UI/runtime behavior.
- Rollback plan.
- Documentation updates when behavior changes.

Use `docs/engineering/definition-of-done.md` as the review checklist.

## Coding guidelines

- Prefer existing helpers such as `spark/jobs/common.py`.
- Keep POC examples readable before making them clever.
- Put reusable patterns in templates or docs, not only in one-off scripts.
- Do not commit secrets, generated caches, `.DS_Store`, or local warehouse data.
- Keep Spark responsible for Iceberg writes; use Trino for SQL serving and Superset/AI consumption.

