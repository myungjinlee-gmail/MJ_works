---
name: create-github-issue
description: Create and verify a GitHub issue from explicit user requirements and the repository issue template. Use when Codex is asked to open a GitHub issue, including a Task that must be checked for actionable scope and objective acceptance before creation.
---

# Create GitHub Issue

Create one issue whose title, body, labels, and hierarchy preserve the user's
intent and the repository's issue structure. Treat GitHub writes as remote
mutations and do not create or update an issue unless the user explicitly asks
for that action.

Prefer an available GitHub MCP tool. Use a command-line client only when the MCP
tool is unavailable or does not support the required operation.

## Workflow

1. Read every applicable `AGENTS.md` and the matching file under
   `.github/ISSUE_TEMPLATE/` in full. Resolve the repository, issue kind, title,
   labels, body, assignee, and requested parent relationship from explicit user
   input and template metadata. Report conflicting issue-kind signals instead
   of guessing.
2. Search open and closed issues in the target repository for semantic
   duplicates before creating anything. If a plausible duplicate exists, stop
   without writing and show the candidate to the user.
3. Check that the proposed issue is complete for its kind. Report each material
   gap and stop rather than inventing requirements, acceptance outcomes, file
   paths, constraints, labels, or hierarchy.
4. Preview the exact title, body, labels, and parent relationship when they were
   assembled or materially transformed by the skill. Preserve user-supplied
   content and artifact-specific fixed text.
5. Create the issue only within the user's requested repository and scope. Add
   labels and the parent relationship only when they are explicit in the
   request or resolved from the selected repository template.
6. Re-read the created issue and verify its title, body, labels, state, and
   parent relationship against the approved input. Report the issue URL and any
   mismatch; do not create a second issue to repair a failed or ambiguous
   operation.

## Task completeness

For a Task, require enough information to answer all of these questions
objectively:

- Why is the task needed, and which required outcomes define completion?
- What is in scope and out of scope?
- Which known changes are required direct changes or necessary consequential
  changes?
- Are any anticipated supporting tools optional for acceptance and identified
  separately from required changes?
- Which observable outcomes and evidence determine acceptance?
- Which schedule, technical, operational, policy, or out-of-scope constraints
  actually apply?

Accept a Task when an assignee can determine the required result and completion
boundary without inventing another requirement. Reject it as incomplete when a
mandatory behavior, boundary, acceptance outcome, or actual constraint is
missing and must be guessed.

Use objective completeness questions rather than subjective detail levels such
as "moderate." Require an implementation method, work sequence, internal
structure, or exhaustive file list only when it is essential to compatibility,
safety, lifecycle requirements, or an acceptance outcome. Do not turn a
reasonable implementation choice into a mandatory issue requirement.

## Known impact

Separate required direct or consequential changes from anticipated optional
supporting tools. For each anticipated optional tool, state that its inclusion
is not required for acceptance. Do not enumerate its internal schemas,
references, metadata, scripts, or validation contracts as issue requirements;
those details remain subject to Pull Request disclosure and normal quality
review if the tool is included.

Do not require an exhaustive impact inventory unless completeness of that
inventory is essential to compatibility, safety, lifecycle requirements, or an
acceptance outcome. Never invent a path merely to make the issue look complete.

## Authority boundary

Write new narrative in local review drafts and temporary working files in the
language used by the user in the current request. Preserve exact source text
and artifact-specific language requirements when they apply.

After creation, the GitHub issue is the sole authoritative source for its scope
and acceptance intent. Local plans, Pull Request bodies, commit messages, and
supporting-tool contracts may provide context but shall not fill a missing
requirement or create a new obligation. If later work reveals a missing
mandatory requirement, update the GitHub issue through a separately authorized
operation before treating that requirement as part of the work.

Keep GitHub unchanged when the request is only to draft, review, or validate an
issue. Do not create a Pull Request, commit, push, or modify repository files as
part of issue creation unless the user separately requests those actions.

## Output

When blocked, identify the duplicate, missing requirement, conflicting signal,
permission problem, or verification mismatch and confirm that no new issue was
created. On success, link the issue and summarize the verified title, label,
state, and parent relationship.
