# Git Workflow

## Branch strategy

- `main` is the stable integration branch.
- Direct pushes to `main` are prohibited; all changes shall use a Pull Request.
- Working branches shall be created from `main` and identify the related issue.

Recommended branch naming forms:

- `<issue-id>-task-<short-description>`
- `dev/<issue-id>-<short-description>`
- `docs/<issue-id>-<short-description>`

These forms are recommendations for consistency, not enforced requirements.

## Commit messages

Use `(#<issue-number>) <summary>`.

Examples:

- `(#12) add cmake hardware target selection`
- `(#18) handle null display backend`
- `(#21) update architecture overview`
- `(#24) add config parser unit tests`

## Pull Requests

- Each Pull Request shall link at least one GitHub Issue.
- The description shall state the scope, changes, and verification evidence.
- Review approval and the merge decision shall follow the reviewer workflow,
  checklist, and review-summary format in the default Pull Request description.

## Merge rule

- The `Release` and `Coverage` checks shall pass.
- A valid review summary for the current head shall conclude `MERGE` or
  `MERGE WITH FOLLOW-UP`.
- Each deferred finding shall link a follow-up issue before merge.
- Prefer Squash Merge to keep `main` history clean.
- Delete the working branch after merge.
