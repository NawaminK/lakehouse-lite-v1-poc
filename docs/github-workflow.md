# GitHub Workflow

## Branching

Use short-lived branches:

```text
feature/<team>/<short-description>
bugfix/<team>/<short-description>
experiment/<team>/<short-description>
```

Examples:

```text
feature/data/csv-ingestion-template
feature/bi/superset-dashboard-v1
feature/ai/trino-readonly-api
bugfix/platform/superset-trino-driver
experiment/lakehouse/polaris-catalog
```

## Pull request rules

Every change must enter through a pull request. The pull request must include:

1. Objective.
2. Changed files or components.
3. Test command and result.
4. Screenshot or log if the change affects UI/runtime behavior.
5. Linked issue.
6. Rollback plan.

## Main branch protection

Recommended branch protection rules for `main`:

- Do not allow direct push.
- Require pull request before merge.
- Require at least one approving review.
- Require CI status check to pass.
- Do not allow force push.

## CODEOWNERS

`CODEOWNERS` maps folder ownership to teams. Replace placeholder owners such as `@platform-team` with real GitHub teams after the repository is created.

## Definition of done

A pull request is done when:

- The code is in the correct folder.
- Documentation is updated if behavior changed.
- A repeatable test command is provided.
- No new secret is committed.
- Baseline POC still works.
- Required reviewers have approved.
- CI passes.
