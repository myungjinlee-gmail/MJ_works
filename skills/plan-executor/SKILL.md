---
name: plan-executor
description: Execute an approved local plan.yaml produced for a GitHub issue by validating its schema, source hashes, Goal IDs, dependencies, changes, and human-approved verification procedures, then implementing ready goals and recording objective evidence. Use when Codex is asked to run, execute, continue, or resume a plan.yaml while preserving issue.md and plan.md as approved inputs.
---

# Plan Executor

Execute an approved schema version 3 `plan.yaml` as a controlled local
workflow. Treat
`issue.md` and `plan.md` as immutable inputs and `plan.yaml` as the machine
execution contract and progress record.

Prefer an available MCP tool for Git and GitHub operations. Use local Git or a
command-line client only when MCP is unavailable or does not support the
required operation.

## Input contract

Accept an explicit path such as `plan/<issue-number>/plan.yaml`. Read
`references/plan-schema.md` in full, then validate the file with:

```text
python3 scripts/validate_plan.py <plan.yaml> --execution-ready
```

Resolve `issue.md` and `plan.md` relative to the `plan.yaml` directory. Refuse
execution when the schema is unsupported, the plan is not approved, a source
hash differs, a Goal ID or reference is invalid, dependencies form a cycle, or
a started Goal has an incomplete dependency. Also refuse a plan when `issue.md`
contains an unresolved Proposal, when required Goal subsections differ between
`plan.md` and `plan.yaml`, or when changes and verification do not cover the
resolved issue requirements.

## Workflow

1. Read every applicable repository `AGENTS.md`, the requested `plan.yaml`, its
   referenced `issue.md`, and `plan.md` in full.
2. Inspect the worktree and preserve existing changes. Do not assume unrelated
   modifications belong to the plan.
3. Run the execution-ready validator. Do not repair requirements, plan content,
   hashes, approval, IDs, dependencies, changes, or verification static fields
   while acting as executor. Return such changes to `$issue-planner`.
4. Resolve the execution scope:
   - Execute the requested Goal when the user names one.
   - Otherwise execute every pending Goal whose dependencies become completed,
     one Goal at a time in dependency order.
   - When multiple Goals are ready, use their order in the `goals` array.
   - Resume an `in_progress` Goal before starting another Goal.
   - Resume a `blocked` Goal only after the user supplies required manual
     evidence or confirms that its blocker changed. For manual verification,
     evaluate the supplied evidence and set that item to `passed` or `failed`.
     Clear the Goal blocker, return it to `in_progress`, and validate before
     continuing.
   - Stop when the next Goal is blocked or no pending Goal is ready.
5. Before implementation, confirm the Goal's requirement references, plan
   section, `changes`, verification procedures, and applicable repository rules.
   Set only that Goal's `status` to `in_progress` in `plan.yaml` and validate
   again.
6. Execute every declared change point for the selected Goal using its exact
   `path` and `operation`. Do not intentionally modify a tracked or source
   artifact absent from the Goal's `changes`. Do not perform work belonging
   solely to a later Goal, weaken a requirement, or broaden external side
   effects beyond the user's execution request.
   On resume, inspect each declared outcome and apply only unmet change points.
   If verification already has runtime progress, continue from the first item
   that is not `passed`; after a failed item, make only corrective changes
   allowed by the Goal before rerunning it. Never repeat satisfied changes
   merely because the Goal was interrupted.
   Treat paired old-path `delete` and new-path `create` entries that reference
   one another as a single file move while preserving both declared outcomes.
7. Execute verification items in their approved order:
   - For `review`, inspect the declared targets using the approved procedure and
     compare the result with the pass condition.
   - For `command`, run exactly the approved command from its working directory.
     Do not silently add flags, substitute another command, or run an external
     or destructive command without separate authorization.
   - For `manual`, set the item and Goal to `blocked`, record what evidence is
     required, and wait for the user.
   Record objective evidence for every passed or failed item.
8. Mark the Goal `completed` only when every verification item is `passed` and
   contains evidence. If execution otherwise cannot continue, set the Goal to
   `blocked`, record `blocker`, preserve available evidence, and stop.
9. Run the validator after every status or evidence update. Recompute neither
   source hash: `issue.md` and `plan.md` must remain unchanged.
10. Repeat for the next ready Goal and validate `plan.yaml` once more after all
    approved verification is complete.

## Mutation boundary

- Never edit `issue.md` or `plan.md`.
- Never change `schema_version`, source paths, hashes, plan approval, Goal IDs,
  titles, references, dependencies, changes, or verification static fields.
- Modify only implementation artifacts and the selected Goal's runtime fields:
  Goal `status`, optional `blocker`, and verification `status` and `evidence`.
- Modify implementation artifacts only at paths declared by the selected Goal.
  Build outputs and temporary verification artifacts may be generated when the
  plan or repository workflow requires them, but do not treat them as unplanned
  source changes.
- Do not update GitHub, open a Pull Request, commit, push, or perform another
  external write unless the user explicitly requests it.
- When implementation reveals an unstated requirement or plan correction, stop
  and return the artifact to `$issue-planner`; do not encode the assumption in
  implementation or `plan.yaml`.

## Goal states

- `pending`: approved but not started.
- `in_progress`: the single Goal currently being executed.
- `completed`: every verification item passed with evidence.
- `blocked`: execution stopped with a concrete `blocker`.

Do not mark a Goal completed based only on code changes or an unverified claim.
Do not skip a Goal; revise the approved plan through `$issue-planner` instead.

## Output

Lead with completed, blocked, and remaining Goal IDs. Summarize changed files,
verification evidence and the final validator result. State that
`issue.md` and `plan.md` remained unchanged and identify any Goal that must
return to planning.
