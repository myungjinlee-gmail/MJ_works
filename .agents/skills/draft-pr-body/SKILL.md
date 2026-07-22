---
name: draft-pr-body
description: Draft concise English GitHub pull request titles and bodies from the repository workflow, PR template, and current branch diff. Use when Codex is asked to create, rewrite, or review a PR title, description, or body before creating or updating a pull request.
---

# Draft PR Title and Body

## Workflow

1. Read `docs/process/git_workflow.md` and `.github/pull_request_template.md`.
    Preserve the template's section order, headings, fixed wording, and reviewer
    checklist items.
2. Determine the intended base branch from the request or PR metadata. Otherwise,
    use `main` when it exists.
3. Inspect the complete branch change with the merge base, commit log, diff stat,
    changed-file list, and relevant diff content. Check the worktree separately and
    do not treat uncommitted changes as part of the PR unless the user requests it.
4. Identify the related issue from the request, branch name, commit messages, or PR
    metadata. Never invent an issue number.
5. Draft the PR title from the complete change and related issue, following the
    commit message rule in `docs/process/git_workflow.md`.
6. Fill only the author-editable template sections. Remove their HTML guidance
    comments and empty placeholders. Preserve the complete `Review` section
    verbatim unless the user explicitly asks to change the review policy.
7. Recheck the title and every body statement against the diff and available
    verification evidence.

## Writing Rules

- Format the PR title as `(#<issue-no>) <summary>`, for example
  `(#21) update architecture overview`.
- Write a concise title that summarizes the complete PR. Do not copy a branch name
  or an individual commit message without checking it against the complete change.
- Never invent an issue number. When it is unknown, leave `#<issue-no>` unresolved.
- Summarize the outcome and purpose in one or two sentences.
- List only the most important implementation changes, normally two to four bullets.
- Describe behavior and policy rather than enumerating files.
- Use `close #<number>` in the template's Related Issue section when the issue is
  known. Leave the placeholder unresolved when it is not known.
- Do not complete the reviewer checklist or select a review decision in the PR
  description. Preserve that reviewer-facing template content unchanged.
- Do not claim that tests or CI passed without evidence.
- Keep the template structure. Do not add sections unless the user requests them.
- Avoid implementation trivia, repetition, promotional language, and vague claims.

## Output

Return the PR title followed by the completed PR body in a Markdown code block
unless the user requests a file or asks to create or update the pull request. Do
not perform a GitHub write without explicit authorization.
