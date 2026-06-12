# Superset Assets

Use this folder for dashboard specs, screenshots, and future Superset exports.

## Current artifact

| File | Purpose |
|---|---|
| `dashboard_v1_spec.md` | Human-readable dashboard v1 build and validation spec |

## Export practice

When a dashboard is created in Superset:

1. Export it from Superset if the UI supports export in the current image.
2. Store the export under this folder.
3. Add a screenshot or validation note to the PR.
4. Update `dashboard_v1_spec.md` if metrics or charts change.

Do not treat local Superset metadata as durable. `make reset` removes the Superset volume.

