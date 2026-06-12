# AI Learning Path

## Goal

Allow AI applications to query Lakehouse data through Trino safely.

## Recommended first pattern

```text
AI assistant -> read-only SQL validator -> Trino -> Iceberg gold tables -> answer
```

## Guardrails

- Allow only `SELECT` and `SHOW` statements in this POC.
- Block destructive keywords such as `DROP`, `DELETE`, `INSERT`, `UPDATE`, `ALTER`, `CREATE`, `TRUNCATE`, `MERGE`, and `CALL`.
- Block comments and multiple SQL statements.
- Query only `iceberg.gold.*` in early phases.
- Add row limits for detail queries.
- Log every query and error.

## Hands-on tasks

1. Start the optional `ai-assistant` profile.
2. Submit a safe SQL query to `/query`.
3. Confirm that non-SELECT SQL is blocked.
4. Add query logging.
5. Add a natural-language-to-SQL layer later.

## Key files

- `ai-assistant/app/app.py`
- `ai-assistant/README.md`
