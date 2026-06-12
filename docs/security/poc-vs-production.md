# Security: POC vs Production

This repository intentionally favors local learning speed. The settings below are acceptable for a single-machine POC only.

## Acceptable in this POC

- Default credentials such as `admin/admin` and `admin/password`.
- Trino without authentication.
- Airflow standalone mode.
- Airflow access to the Docker socket.
- Local Docker volumes without backup.
- Single-node MinIO.
- Plain HTTP between containers.
- Minimal AI SQL validation without user identity.

## Required before production-like use

- Replace hard-coded credentials with secret management.
- Enable TLS for user-facing and service-to-service traffic.
- Add SSO or another identity provider.
- Add Trino authentication and access control.
- Remove Docker socket access from Airflow.
- Use a production Airflow deployment with a real metadata database.
- Use durable object storage or distributed MinIO.
- Add backup, restore, and disaster recovery drills.
- Add audit logging for SQL, dashboard, orchestration, and AI access.
- Add row-level/table-level authorization where business data requires it.

## AI query API guardrails

The AI assistant is a prototype. It should remain read-only and should not become a general SQL execution service.

Current POC stance:

- Allow `SELECT` and `SHOW`.
- Block common destructive keywords.
- Limit returned rows.

Production stance:

- Authenticate every caller.
- Authorize schemas and tables per user.
- Log every query and error.
- Add query timeouts and cost limits.
- Evaluate generated SQL before execution.
- Prefer curated semantic/query templates for business users.

