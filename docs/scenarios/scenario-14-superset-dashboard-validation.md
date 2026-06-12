# Scenario 14: Superset Dashboard Validation

Goal: verify the analyst consumption path.

Manual steps:

1. Open `http://localhost:8088`.
2. Log in with `admin/admin`.
3. Add Trino database URI `trino://admin@trino:8080/iceberg`.
4. Create a dataset from schema `gold`, table `daily_sales`.
5. Build charts for net sales by province and net sales by date.

Pass criteria:

- Superset connects to Trino.
- Dataset columns are visible.
- Charts refresh without query errors.

Dashboard spec:

- `superset/assets/dashboard_v1_spec.md`

