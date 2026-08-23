---
name: draft-pr-body
description: Draft concise GitHub pull request titles and bodies from the repository workflow, PR template, and current branch diff. Use when Codex is asked to create, rewrite, or review a PR title, description, or body before creating or updating a pull request.
---

# Draft PR Title and Body

## Workflow

1. Prefer an available MCP tool for Git and GitHub operations. Use local Git or
    a command-line client only when MCP is unavailable or does not support the
    required operation.
2. Read `docs/process/git_workflow.md`,
    `docs/design/requirement/README.md`, and
    `.github/pull_request_template.md`.
    Preserve the template's section order, headings, fixed wording, and reviewer
    checklist items.
3. Determine the intended base branch from the request or PR metadata. Otherwise,
    use `main` when it exists.
4. Inspect the complete branch change with the merge base, commit log, diff stat,
    changed-file list, and relevant diff content. Check the worktree separately and
    do not treat uncommitted changes as part of the PR unless the user requests it.
5. Identify the related issue from the request, branch name, commit messages, or PR
    metadata. Never invent an issue number. Determine whether this Pull Request
    completes that issue or only references work that continues in later Pull
    Requests.
6. Use only the linked GitHub Issue and repository policies as authoritative
    sources for requirements, acceptance criteria, and scope. Local plans may
    identify changed files or provide non-authoritative context, but shall not
    add requirements or acceptance criteria. Classify every file in the complete
    diff as direct implementation, necessary consequential policy or
    documentation, an eligible optional supporting tool, or unrelated work.
    Apply the eligibility and precedence rules in `docs/process/git_workflow.md`.
    Treat an unclear classification, an unsupported eligibility claim, and any
    unrelated or ineligible change as an unresolved scope problem.
7. When the change concerns an SWR, SWRVS, downstream implementation, or
    verification implementation, read the applicable authoring rules and verify
    that the diff follows the requirement Pull Request sequence. Require a new
    SWR and all SWRVS artifacts needed to cover it in one authoring Pull Request.
    Require a semantic SWR change and every affected AC or VM change together.
    Permit an SWRVS-only correction when the SWR does not change, and permit a
    later stage's required trace-only update. Report authoring mixed with
    downstream or verification implementation as a scope problem.
8. Draft the PR title from the complete change and related issue, following the
    commit message rule in `docs/process/git_workflow.md`.
9. Fill only the author-editable template sections. Remove their HTML guidance
    comments and empty placeholders. Preserve the complete `Review` section
    verbatim unless the user explicitly asks to change the review policy. In
    `Supporting Tools`, write `None` when there is no eligible optional tool.
    Otherwise, disclose every tool's path or identifier, reason for addition,
    relationship to the linked issue, evidence that it has no product,
    requirements, design, or lifecycle impact, and verification results.
10. Recheck the title and every body statement against the diff and available
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
- Preserve every checklist `<details>` element. Do not expand or duplicate its
  checklist in an author-editable section.
- Do not claim that tests or CI passed without evidence.
- Keep the template structure. Do not add sections unless the user requests them.
- Avoid implementation trivia, repetition, promotional language, and vague claims.
- Write new narrative in local PR drafts and temporary working files in the
  language used by the user in the current request.
- Before creating or updating a remote Pull Request, explicitly ask the user to
  confirm the target language and wait for both that choice and separate
  authorization for the remote write. Use the confirmed language for new remote
  narrative.
- A content-language change shall not translate or otherwise alter this skill's
  Markdown headings, the Pull Request template's headings or fixed wording,
  machine-readable tokens, commands, code, or quoted source text.

## Output

Return the PR title followed by the completed PR body in a Markdown code block
unless the user requests a file or asks to create or update the pull request. Do
not perform a GitHub write without explicit authorization.
