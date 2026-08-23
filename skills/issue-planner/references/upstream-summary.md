# Upstream Issue Summary

Use this optional mode to project resolved local requirements into a concise
GitHub issue contract for Pull Request review. Never use the web summary as an
input to `plan.md` or `plan.yaml`.

## Managed block

```markdown
<!-- issue-planner:summary:start -->

## Planning summary

### Purpose

<concise purpose>

### Scope

- <included result or important exclusion>

### Expected outcomes

- <externally or review-visible outcome>

### Acceptance summary

- <high-level pass condition>

### Detailed requirements

See `plan/<issue-number>/issue.md` in the related Pull Request.

<!-- issue-planner:summary:end -->
```

## Semantic alignment

Confirm all of these before offering an update:

- Purpose and scope do not contradict or materially narrow or broaden local
  requirements.
- Expected outcomes cover behavior needed to judge Pull Request scope.
- Acceptance summary agrees with local Verification and acceptance without
  copying commands or procedures.
- The summary introduces no mandatory behavior absent from `issue.md`.
- Exact file paths, Goal IDs, implementation steps, commands, detailed
  verification, and Proposal history stay local. The detailed-requirements
  path is the only planned local path in the managed block.
- No `TBD`, `TODO`, `Pending`, angle-bracket placeholder, or authoring
  instruction remains in a publishable summary.
- The detailed-requirements path exists, uses the same issue number as the
  GitHub issue, and is intended to be included in the related Pull Request.
- The related Pull Request identifies the same GitHub issue according to the
  repository Pull Request template. Report a missing or different link; do not
  mutate the Pull Request in this mode.

Read the repository Pull Request template and every applicable review
checklist. When they use checks such as `SCOPE`, `TRACE`, and `VERIFY`, report
the evidence chain:

```text
GitHub issue summary
    -> local issue.md requirements
    -> plan Goal and changes
    -> verification and evidence
```

The initial ticket may remain abstract when requirement artifacts link it as
their upstream source and retain the detailed, objective obligations locally.

## Script input

Pass this shape to `scripts/issue_summary.py build`:

```json
{
    "body": "<current GitHub issue body>",
    "summary": {
        "purpose": "<concise purpose>",
        "scope": ["<scope result or important exclusion>"],
        "expected_outcomes": ["<review-visible outcome>"],
        "acceptance_summary": ["<high-level pass condition>"],
        "detailed_requirements": "plan/<issue-number>/issue.md"
    }
}
```

All arrays shall be non-empty. Add the complete generated body as `candidate`
when calling `verify` with the same input.

## Publication procedure

1. Generate the structured summary from resolved `issue.md`.
2. Use `scripts/issue_summary.py build` with the freshly read GitHub issue body.
3. Print the exact managed block, complete proposed body, and semantic-alignment
   assessment before any external write.
4. Obtain explicit user approval for that exact update. Approval to plan or to
   resolve Proposals is not approval to update GitHub.
5. Re-read the GitHub issue immediately before writing. If its body differs
   from the input used to build the candidate, discard the candidate and stop
   for a new preview.
6. Update only the issue body. Add the block when absent or replace the one
   existing block. Preserve every byte outside it. Never change the title,
   labels, assignees, state, hierarchy, milestone, or comments in this mode.
7. Re-read the issue and use `scripts/issue_summary.py verify` against the
   published body. Report the issue URL and review-check evidence. Do not change
   `issue.md`, `plan.md`, or `plan.yaml` as a consequence of publication.

After later local edits, reassess the projection before Pull Request review.
Update GitHub only when Purpose, scope, expected outcomes, or acceptance intent
changed. Implementation-only detail does not make the web summary stale.
