# Contributing

This POC is a team learning project. Keep changes small, linked to an issue, and easy to verify.

## Start

```bash
cp .env.example .env
make up
make smoke
```

If setup fails, check `docs/runbooks/troubleshooting.md` before changing code.

## Pick Work

1. Choose an issue from the [Project Board](https://github.com/users/NawaminK/projects/3).
2. Read the related requirement in `docs/requirements.md`.
3. Read your team path in `docs/team-getting-started.md`.
4. Move the issue to In Progress.

## Branches

Use short-lived branches:

```text
feature/<team>/<short-description>
bugfix/<team>/<short-description>
experiment/<team>/<short-description>
```

Examples:

```text
feature/team-b/csv-ingestion-template
feature/team-c/dashboard-v1
bugfix/team-a/trino-readiness
experiment/team-d/nifi-ingestion-note
```

## Pull Requests

Every PR should include:

- Linked issue and requirement ID.
- Team/area checkbox.
- Narrow validation evidence.
- Documentation update or reason it was not needed.
- Risk and rollback plan.

Use:

- `.github/pull_request_template.md`
- `docs/engineering/definition-of-done.md`
- `docs/github-workflow.md`

## Validation

Run the narrowest useful check:

```bash
make validate
make smoke
make scenarios
python -m unittest discover -s ai-assistant/tests
```

For docs-only changes, `make validate` is usually enough.

## Ground Rules

- Do not commit secrets, generated caches, `.DS_Store`, or local warehouse data.
- Prefer existing helpers before adding new patterns.
- Keep Spark responsible for Iceberg writes.
- Use Trino for SQL serving and Superset/AI consumption.
- Update docs when commands, ports, services, or behavior change.
