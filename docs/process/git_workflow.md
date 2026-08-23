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
- The linked GitHub Issue is the sole authoritative source for the Pull
  Request's requirements and acceptance criteria. Local plans and other
  supporting artifacts may provide context, but shall not add or change them.
- The description shall state the scope, changes, and verification evidence.
- Classify every changed file into exactly one scope category:
  1. direct implementation of the linked issue;
  2. necessary consequential policy or documentation updates;
  3. eligible optional supporting tools; or
  4. unrelated work.
- Only categories 1 through 3 pass the `SCOPE` review check. Category 4 shall
  be moved to a separate issue and Pull Request.
- A category 3 supporting tool is eligible only when it is discovered or
  created while implementing the linked issue, is optional for acceptance,
  does not change product behavior, the linked issue's requirements or
  acceptance criteria, design interfaces, repository lifecycle rules, CI,
  review, merge, release, or external-write permissions, does not establish a
  repository-wide policy or make itself or its internal contract a mandatory
  product, requirement, design, CI, review, merge, release, or lifecycle rule,
  and is isolated, reviewable, verified, and disclosed in the Pull Request
  description.
- An eligible supporting tool may define internal schemas, references,
  metadata, helper scripts, state models, and validation contracts needed for
  its explicit opt-in operation. These internal contracts remain part of the
  category 3 tool, do not become Pull Request requirements or acceptance
  criteria, and shall not become repository-wide prerequisites. Tool-specific
  self-tests and validation evidence support normal quality review and do not
  become independent product or repository-process acceptance criteria.
- Create a separate issue or update the linked issue before including a tool
  that adds or changes repository-wide normative workflow behavior, becomes a
  prerequisite for issue acceptance or a repository lifecycle verification
  step, needs independent product or repository-process acceptance criteria,
  or bypasses or weakens a required repository lifecycle boundary.
- Repository and applicable domain policies take precedence over supporting
  artifacts and cannot be relaxed by the scope classification.
- A normal working branch shall target `main`.
- A release work branch shall target its owning release branch.
- A release branch shall target `main` when integrating completed release
  changes.
- Review approval and the merge decision shall follow the reviewer workflow,
  checklist, and review-summary format in the default Pull Request description.
- Requirement changes shall follow the Pull Request sequence in
  [Software Requirements and Verification](/docs/design/requirement/README.md#requirement-development-sequence).

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
