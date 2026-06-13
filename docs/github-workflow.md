# GitHub Workflow

Use GitHub as the execution layer: issues define work, the Project Board shows status, pull requests carry review and validation evidence.

## Flow

1. Pick an issue from the [Project Board](https://github.com/users/NawaminK/projects/3).
2. Confirm the requirement ID in `docs/requirements.md`.
3. Create a short-lived branch.
4. Make a small change.
5. Run the narrowest useful validation.
6. Open a PR using `.github/pull_request_template.md`.
7. Move the issue through Todo -> In Progress -> Done.

## Branches

```text
feature/<team>/<short-description>
bugfix/<team>/<short-description>
experiment/<team>/<short-description>
```

Examples:

```text
feature/team-b/csv-ingestion-template
feature/team-c/superset-dashboard-v1
bugfix/team-a/service-readiness
experiment/team-d/hop-pipeline-note
```

## Pull Request Expectations

Every PR should include:

- Linked issue.
- Requirement ID or exploratory note.
- Team/area.
- Validation evidence.
- Documentation impact.
- Risk and rollback plan.

## Branch Protection Recommendation

Recommended rules for `main`:

- Require pull request before merge.
- Require at least one approving review.
- Require CI status checks to pass.
- Do not allow force pushes.
- Delete branches after merge.

## CODEOWNERS

`CODEOWNERS` maps folders to team owners. Replace placeholder owners such as `@platform-team` with real GitHub teams when they exist.

## Done Means

- The issue acceptance criteria are met.
- The related requirement is still accurate.
- Validation evidence is in the PR.
- Docs are updated when behavior changes.
- CI passes and required reviewers approve.
