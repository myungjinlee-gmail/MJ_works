---
name: review-pull-request
description: Review or re-review GitHub pull requests using the repository's `.github/pull_request_template.md` workflow, checklist, and decisions. Use when Codex is asked to assess PR readiness, inspect a PR for defects, prepare or submit line-specific review threads, request changes, approve a PR, or produce the required review summary.
---

# Review Pull Request

Review the current PR head against its issue, repository policies, changed
behavior, and verification evidence. Treat `.github/pull_request_template.md`
as the source of truth; do not copy its checklist into this skill.

## Review workflow

1. Read repository instructions and `.github/pull_request_template.md` in full.
   Use the base-branch version as the governing rules when the PR changes the
   template itself; review the proposed template version as part of the diff.
2. Identify the repository, PR number, base, current head SHA, author, draft
   state, linked issues, and authenticated GitHub user. Call GitHub `get_me`
   before other GitHub operations.
3. Read the linked issue and relevant coding, architecture, testing, and process
   documents. Inspect the complete PR diff, changed files, commits, existing
   reviews, and review threads.
4. Fetch check runs for the current head and use them as the CI source of truth.
   Start the review only when every check run is completed successfully. If any
   check is missing, pending, skipped, cancelled, or failed, stop and report the
   exact check state without posting a review. Do not treat an empty legacy
   combined-status result as pending when check runs contain the repository's
   CI results; report the API discrepancy instead.
5. Determine the review scope:
   - For an initial review, inspect the complete base-to-head change.
   - For a re-review, find the authenticated reviewer's latest valid submitted
     review commit and inspect changes from that commit through the current
     head. A valid prior review contains the template checklist with every row
     completed and exactly one decision; ignore casual or partial comments.
   - Use `CODEOWNERS`, repository ownership documentation, requested-reviewer
     context, or explicit user context to identify owned areas. On re-review,
     review only new changes in areas owned by the current reviewer; retain
     approvals for unaffected areas.
   - If ownership cannot be determined, inspect all new changes and state that
     ownership could not be narrowed.
6. Trace requirements through implementation, tests, documentation, and build
   configuration. Prioritize correctness, safety, regressions, error paths,
   interface compatibility, ownership/lifetime, concurrency, and missing tests.
7. Reconcile existing threads before creating findings. Confirm whether each
   prior request is resolved in the current scope and avoid duplicating an
   active thread.
8. Complete every checklist row from the PR template as `PASS`, `FAIL`, or
   justified `N/A`. Base each result on inspected evidence; do not infer that a
   test or check passed.
9. Select exactly one decision using the template criteria:
   - `DO NOT MERGE` when any required item fails, evidence is missing, a CI
     check is not successful, or a blocking finding remains.
   - `MERGE` when all required items pass or have justified `N/A` results and no
     blocking finding remains.
   - `MERGE WITH FOLLOW-UP` only when acceptance criteria pass, findings are
     non-blocking, and each deferred finding links an existing follow-up issue.

## Findings

Write only actionable findings caused by the PR. Attach each change request to
the narrowest relevant changed line. Use a file-level thread only when no single
line represents the problem.

Format each finding as:

```markdown
[BLOCKING] F-001: <concise problem>

<why this is a problem and the concrete failure mode>

Required change: <specific outcome required>
```

Use `NON-BLOCKING` only when the finding does not violate acceptance criteria,
create correctness or safety risk, or leave required verification incomplete.
Include the follow-up issue link in a deferred finding.

Do not modify the PR branch while acting as reviewer. Do not resolve an author's
thread until the current diff demonstrates that the requested outcome is met.

## GitHub submission

Treat review submission as an external write. Inspect and draft the review when
the user asks only to review; post threads or submit a GitHub review only when
the user explicitly requests posting, submission, approval, or change requests.

For an authorized review with line findings:

1. Create a pending review with `pull_request_review_write` method `create` and
   the current head SHA. If the authenticated reviewer already has a pending
   review, reuse it.
2. Add every finding with `add_comment_to_pending_review`. Use `RIGHT` for added
   or changed lines and `LEFT` for deleted lines.
3. Copy the review-summary block from `.github/pull_request_template.md`, fill
   every checklist result, select one decision, and replace every placeholder.
4. Submit the pending review with:
   - `REQUEST_CHANGES` for `DO NOT MERGE`;
   - `APPROVE` for `MERGE` or `MERGE WITH FOLLOW-UP`;
   - `COMMENT` only when GitHub prevents the required approval, such as an
     author reviewing their own PR. Report that limitation explicitly.
5. Re-read the PR reviews and threads to verify that the submitted event,
   summary, and line comments are present on the intended head.

For an authorized review without findings, a pending review is still preferred
so the same summary and verification sequence is used consistently.

## Output

Lead with the decision. List blocking findings before non-blocking findings,
include file and line references, summarize CI evidence, and state whether the
review was drafted or submitted. If submitted, link the PR and identify the
reviewed head SHA.
