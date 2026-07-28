# Git Workflow

## Branch strategy

- `main` is the stable integration branch.
- `main` and every `release/**` branch shall be protected.
- Direct pushes, force pushes, history rewrites, and deletion are prohibited on
  protected branches. All changes shall use a Pull Request.
- Normal working branches shall be created from `main`.
- Each independently released project shall use one release branch per
  supported major version, created from `main`:

```text
release/<project>/<major>.x
```

- Work for an existing major version shall use a development branch created
  from the target release branch:

```text
dev/<project>/<issue>-<short-description>
```

- A release branch shall maintain linear history. A release work branch shall
  enter it only with Squash Merge.
- A release branch shall be retained as protected, read-only historical
  evidence after its major version reaches end of support.

Recommended branch naming forms:

- `<issue-id>-task-<short-description>`
- `dev/<issue-id>-<short-description>`
- `dev/<project>/<issue-id>-<short-description>`
- `docs/<issue-id>-<short-description>`

Use the project-qualified `dev` form for a branch targeting a release branch.
The other forms are recommendations for consistency.

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
- A normal working branch shall target `main`.
- A release work branch shall target its owning release branch.
- A release branch shall target `main` when integrating completed release
  changes.
- Review approval and the merge decision shall follow the reviewer workflow,
  checklist, and review-summary format in the default Pull Request description.

## Merge rule

- The `Release` and `Coverage` checks shall pass.
- A valid review summary for the current head shall conclude `MERGE` or
  `MERGE WITH FOLLOW-UP`.
- Each deferred finding shall link a follow-up issue before merge.
- A release work branch entering a release branch shall use Squash Merge.
- A release branch entering `main` shall use a merge commit. Squash Merge and
  Rebase Merge are prohibited for this direction so tagged release commits keep
  the same hashes in the ancestry of `main`.
- All other branches entering `main` should use Squash Merge to keep normal
  development history concise.
- Delete normal and release work branches after merge. Do not delete release
  branches.
