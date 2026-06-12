# AI Assistant POC

This service exposes a minimal read-only API for AI applications that need to query Lakehouse data through Trino.

## Start

```bash
docker compose --profile ai up -d --build ai-assistant
```

## Health check

```bash
curl http://localhost:8010/health
```

## Query Trino

```bash
curl -X POST http://localhost:8010/query \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT province, SUM(net_sales) AS total_net_sales FROM daily_sales GROUP BY province ORDER BY total_net_sales DESC"}'
```

## Guardrails

- Allows `SELECT` and `SHOW` only.
- Blocks destructive keywords such as `DROP`, `DELETE`, `INSERT`, `UPDATE`, `ALTER`, `CREATE`, `TRUNCATE`, `MERGE`, and `CALL`.
- Blocks comments and multiple SQL statements.
- Uses Trino as the controlled SQL access layer.
- Intended for POC only; production needs authentication, authorization, query logging, row limits, and prompt evaluation.

## Tests

```bash
PYTHONPATH=ai-assistant python -m unittest discover -s ai-assistant/tests
```
