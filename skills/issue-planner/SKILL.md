---
name: issue-planner
description: Create authoritative local requirements and an executable plan from a GitHub issue, refine issue.md through actionable add, replace, or remove Proposals, and optionally publish a compact semantically aligned GitHub issue summary after explicit approval. Use when Codex is asked to inspect, refine, plan, or prepare review traceability for a GitHub issue, task, bug, change request, or Epic.
---

# Issue Planner

Turn one abstract GitHub issue into authoritative local requirements and an
implementation plan. Keep the boundary strict: the GitHub issue states concise
purpose, scope, outcomes, and acceptance intent; `issue.md` says in detail what
must be done; `plan.md` says how to do it. Treat GitHub as read-only by default.

Prefer an available MCP tool for Git and GitHub operations. Use local Git or a
command-line client only when MCP is unavailable or does not support the
required operation.

## Artifact contract

Create these files under the repository root:

```text
plan/<issue-number>/
├── issue.md
├── plan.md
└── plan.yaml
```

Use the decimal GitHub issue number as `<issue-number>` without `#` or a title
slug.

### `issue.md`

When `issue.md` does not exist, seed it from the GitHub issue:

```markdown
# <exact GitHub issue title>

<exact GitHub issue body>
```

Verify this initial seed exactly. After creation, make `issue.md` the
authoritative local requirements artifact. It may intentionally become more
detailed than the GitHub issue through accepted Proposals. Do not require
byte-for-byte equality, merge upstream text into it, or overwrite local detail
to match the web issue.

Treat only resolved local issue text as normative requirements. Treat every
complete Proposal block, including its Action, Target, Proposed change, and
Rationale, as a non-normative review annotation. Never derive a plan while a
Proposal remains in `issue.md`. Keep implementation steps, commands, estimates,
and sequencing out of `issue.md` unless the source issue explicitly requires
them.

### Requirement completeness

Use the issue Purpose as the primary Proposal criterion. Add a Proposal when
the Purpose cannot be achieved from the existing Detailed requirements, Known
impact, constraints, and Verification and acceptance requirements without
inventing an assumption. Require this trace before planning:

```text
Purpose
    -> Detailed requirements
    -> Known impact
    -> Verification and acceptance
```

Supplement Detailed requirements when a mandatory behavior, boundary,
constraint, trace relationship, or objectively verifiable outcome needed by
the Purpose is absent. Keep requirements focused on required results rather
than implementation sequencing.

Propose `replace` when existing issue text is partly incorrect and a corrected
requirement is known. Propose `remove` only when the exact target text
contradicts the Purpose or another resolved requirement, is factually
inconsistent with inspected repository evidence, is superseded or duplicated,
falls outside the issue scope, or would otherwise cause unnecessary work. Use
`add` for missing content. Do not remove merely vague or incomplete content
when it can be made correct with `replace`.

Require Known impact to identify every file that must be created, modified, or
deleted. Put each exact repository-relative file path first and list its
operation and modification points underneath:

```markdown
### Known impact

- `path/to/file.ext`
    - Operation: modify
    - <specific modification point>
    - <additional modification point>
```

Use only `create`, `modify`, or `delete` as the operation. Represent a file move
as two entries: `delete` for the old path and `create` for the new path. Put the
counterpart path in each entry's modification point so the pair is
unambiguous.

Make every modification point a concrete, independently checkable result. Do
not use a directory, glob, placeholder, unresolved path, or an invented file.
When repository inspection cannot determine the exact file, stop and report
the unresolved impact instead of approving a plan.

### `plan.md`

Derive `plan.md` only from the normative requirements in `issue.md`. Include:

1. the objective and requirement references;
2. affected files, modules, interfaces, and artifacts;
3. ordered implementation steps;
4. verification and acceptance steps;
5. dependencies, risks, and unresolved blockers.

Trace each plan step to a resolved issue section. Do not create a new
requirement or weaken a constraint. When a plan needs an unstated requirement
or assumption, stop planning and return to the Proposal workflow.

Give every top-level implementation Goal a stable heading:

```markdown
## G-001: <Goal title>
```

Allocate Goal IDs in ascending order, preserve them across revisions, and do
not renumber them when ordering changes.

Under every Goal, reproduce its file work using the Known impact shape:

```markdown
### Changes

- `path/to/file.ext`
    - Operation: modify
    - <specific modification point from Known impact>
```

Every Known impact modification point shall appear in exactly one Goal. A path
may appear in multiple Goals only when its modification points are
non-overlapping. Do not add a plan file or point that is absent from resolved
`issue.md`.

Give every Goal these required subsections and keep their values identical to
`plan.yaml`:

```markdown
### Requirements

- `issue.md#detailed-requirements`

### Dependencies

None.

### Changes

...

### Verification and acceptance

- `G-001-V-01`: <verification title>
    - Method: review
    - Requirement: `issue.md#verification-and-acceptance`
    - Target: `path/to/file.ext`
    - Procedure: <what the executor shall inspect>
    - Pass condition: <objective success condition>
```

For dependencies, write `None.` or one backticked Goal ID per list item. Keep
verification runtime status and evidence only in `plan.yaml`.

Derive every verification item from resolved `Verification and acceptance`
requirements in `issue.md`. Use `review` when the executor can inspect files,
diffs, or behavior; use `command` for an approved local build, test, lint, or
other non-destructive command; use `manual` only when human or external-system
evidence is unavoidable. Put the exact command and working directory in
`plan.md`. If the required procedure or pass condition cannot be determined,
return to the Proposal workflow.

### `plan.yaml`

Generate schema version 3 `plan.yaml` as the machine execution contract for
`plan.md`. Read
`../plan-executor/references/plan-schema.md` in full and use the same Goal IDs,
titles, file changes, modification points, Goal requirement references,
dependencies, and verification static fields in both files. Include SHA-256
hashes of the exact `issue.md` and `plan.md` bytes.

Create a new plan with `plan.status: "draft"`. After the user reviews and
accepts the human-readable `plan.md`, change only that field to `"approved"`.
Validate the manifest with
`../plan-executor/scripts/validate_plan.py`; do not hand off an invalid or draft
plan to `$plan-executor`.

## Workflow

1. Read every applicable repository `AGENTS.md` and identify the repository and
   issue number.
2. Read the GitHub issue title, body, and metadata as abstract purpose and scope
   context. Read comments, hierarchy, and linked Pull Requests only when they
   affect the Purpose or requirements.
3. Resolve `plan/<issue-number>/issue.md`, `plan.md`, and `plan.yaml`. Before
   creating any file, inspect existing files and preserve user changes.
4. When `issue.md` does not exist, create it from the exact title and body using
   `scripts/proposal_blocks.py issue-md`. Verify it immediately with
   `verify-issue-md`. This exactness check applies only to initial seeding.
5. When `issue.md` exists, preserve it as the local source of truth. Check only
   that its Purpose and scope do not contradict explicit GitHub issue intent.
   Local detail absent from GitHub is expected. If GitHub changes materially,
   report the semantic conflict and use the Proposal workflow for any local
   requirement change; do not reconcile or overwrite either artifact.
6. When the issue structure identifies a repository issue template, read that
   template in full. Resolve the issue kind from its label, title prefix, and
   body structure; report conflicting signals instead of guessing.
7. Read the repository files, process rules, and linked artifacts needed to
   verify the issue. Check that it is actionable, internally consistent,
   current, traceable, and objectively verifiable. For an Epic, reconcile the
   task list with actual sub-issues and states. For a Task, require concrete
   impact, specific requirements, verification, and constraints.
8. Trace the Purpose through Detailed requirements, Known impact, and
   Verification and acceptance. Create `add`, `replace`, or `remove` Proposals
   only for material changes needed to make that trace correct and complete.
   Prioritize missing or incorrect Known impact and mandatory Detailed
   requirements. Make each Proposed change immediately actionable. Do not
   restate adequate text, invent paths or evidence, or add a Proposal merely to
   show activity.
9. If at least one Proposal is required, build the complete `issue.md`
   candidate with `scripts/proposal_blocks.py build`. Print the exact new or
   revised Proposal blocks as text before writing them. Re-read `issue.md`; if
   it changed, discard the candidate and rebuild it. Insert the blocks at their
   previewed targets and verify the result with the script without waiting for
   Proposal approval. If no Proposal is required, leave `issue.md` unchanged
   and continue.
10. Before generating a plan, scan `issue.md` for Proposal boundary markers,
    visible Proposal labels, and legacy `[Proposal]` headings. If any Proposal
    remains, do not create or update `plan.md` or `plan.yaml`. Ask the user to
    accept, revise, or reject it locally. After an explicit decision, use
    `scripts/proposal_blocks.py resolve`: accepted `add`, `replace`, and
    `remove` actions update local normative text; rejection removes only the
    Proposal block. Re-read the result and ensure the selected block is gone.
    Do not require or perform a matching GitHub update.
11. Confirm resolved Known impact contains exact file paths, one allowed
    operation per file, and concrete modification points. Confirm
    `Verification and acceptance` defines objectively checkable outcomes. Do
    not generate an approvable plan while either mapping is unresolved.
12. Generate or update `plan.md` from the resolved `issue.md`. Assign every
    Goal a stable `G-NNN` ID and decompose its work into exact Known impact
    files and points under `Changes`. If planning exposes a missing requirement
    or file, add another Proposal and return the issue to the user instead of
    encoding the assumption in `plan.md`; regenerate only after every Proposal
    is resolved.
13. Generate schema version 3 `plan.yaml` with `status: "draft"`, matching Goal
    IDs, Goal requirement references, dependencies, file changes, points,
    verification static fields, and source hashes. Run the plan validator
    without `--execution-ready`. If generated artifacts disagree, repair them
    from resolved `issue.md` and rerun validation without asking the user to
    correct generator output. Stop and return to Proposal review only when the
    correction would require a new requirement or assumption. Show `plan.md`
    to the user as the review surface, including every command the executor may
    run.
14. After explicit plan approval, confirm neither source file changed, set
    `plan.status` to `"approved"`, and run the validator with
    `--execution-ready`.
15. Re-read all three files and verify their role boundary, traceability, Goal
    and change parity, Known impact coverage, hashes, semantic compatibility
    with the abstract GitHub issue, and lack of unresolved placeholders before
    reporting completion.

## Optional upstream summary

Planning never requires GitHub and `issue.md` to contain the same level of
detail. When the user requests review-ready issue traceability, project policy
requires it, or a Pull Request is being prepared, offer a compact semantic
projection of resolved `issue.md`. The web summary is not a planning input and
does not replace local requirements. Read `references/upstream-summary.md` in
full before generating, previewing, publishing, or verifying this summary.

## Proposal format

Allocate IDs in ascending order within `issue.md`. Preserve existing IDs and
continue after the highest number. Use one of `add`, `replace`, or `remove` as
the Action. Target the smallest exact, unique local fragment that makes the
change location unambiguous. For `replace` and `remove`, Target is the complete
current local content affected; for `add`, it is the exact insertion anchor. Use
explicit boundary markers and non-heading labels so nearby original content
does not become part of the Proposal:

```markdown
<!-- proposal:P-001:start -->

**[Proposal] P-001: <concise proposed change>**

**Action**

<add | replace | remove>

**Target**

> <exact local content or insertion anchor>

**Proposed change**

<final Markdown to add or substitute; use exactly `None.` for remove>

**Rationale**

<evidence-backed reason for the proposal>

<!-- proposal:P-001:end -->
```

For `add` and `replace`, write Proposed change as non-empty final issue Markdown
in the issue's language and style. For `remove`, use exactly `None.`; Action and
Target then mean that the complete Target shall be removed without replacement.
If replacement text is required, use `replace` instead. Do not use tentative
meta-instructions such as "define", "clarify", or "consider". Do not add
acceptance checkboxes. Insertion records an unresolved review item, not
acceptance of its content.

For local resolution, pass the current `issue.md` as `candidate`, the exact
rendered Proposal fields as `proposal`, and `accept` or `reject` as `decision`
to `scripts/proposal_blocks.py resolve`. Preview the resolved candidate before
writing it, re-read the file before application, and leave every other Proposal
unchanged.

## Preservation rules

- Write new narrative in local planning drafts and temporary working files in
  the language used by the user in the current request. Preserve exact source
  text and artifact-specific language requirements when they apply.
- Before publishing a managed GitHub issue summary or other formal remote
  content, explicitly ask the user to confirm the target language and wait for
  both that choice and separate authorization for the remote write. Use the
  confirmed language for new remote narrative.
- A content-language change shall not translate or otherwise alter this skill's
  Markdown headings, fixed source or template text, machine-readable tokens,
  commands, code, or quoted source text.
- Leave GitHub unchanged by default. The optional managed-summary procedure is
  the only allowed issue mutation.
- Preserve current local text outside deliberate Proposal insertion and
  user-approved local Proposal resolution.
- Target each Proposal at exact, unique current `issue.md` text. Refuse an
  ambiguous or missing target instead of guessing. Every Proposal target must
  be exclusive; combine changes that need the same target.
- Never place a Proposal inside another Proposal block or duplicate an existing
  ID or materially equivalent proposal.
- Treat a Proposal as beginning and ending only at its matching explicit
  boundary markers. Refuse malformed, nested, or mismatched markers.
- Never overwrite an existing `issue.md`, `plan.md`, or `plan.yaml`; preserve
  and deliberately revise its current local content.
- Use `scripts/proposal_blocks.py` to construct and verify issue documents and
  Proposal candidates whenever the content can be passed without unsafe shell
  interpolation.
- Treat GitHub-to-local exactness as an initial-seed invariant only. Do not add
  synchronization or reconciliation checks to planning or execution.

## Output

Print Proposal blocks in insertion order before writing them. After inserting
any Proposal, state that planning is blocked until the user resolves it and
that `plan.md`, `plan.yaml`, and GitHub are unchanged. After plan generation,
link all three files, list Goal IDs, summarize semantic alignment and validator
results, and state whether the plan is draft or approved. For optional upstream
publication, show the preview and approval state, then report whether the
managed block was verified or GitHub remained unchanged.
