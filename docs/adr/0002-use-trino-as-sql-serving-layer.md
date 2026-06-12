# ADR 0002: Use Trino as SQL serving layer

## Status

Accepted for POC.

## Context

The POC needs a SQL engine that can serve BI dashboards, ad hoc analytics, and AI read-only SQL access.

## Decision

Use Trino with the Iceberg connector.

## Consequences

- Superset can query Iceberg tables through Trino.
- AI assistants can query through a controlled SQL layer.
- Trino catalog configuration and S3 connectivity become critical platform dependencies.
