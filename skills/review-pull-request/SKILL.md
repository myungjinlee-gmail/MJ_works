---
name: review-pull-request
description: Review or re-review GitHub pull requests using the repository's `.github/pull_request_template.md` workflow, checklist, and decisions. Use when Codex is asked to assess PR readiness, inspect a PR for defects, prepare or submit line-specific review threads, request changes, approve a PR, or produce the required review summary.
---

# Review Pull Request

Review the current PR head against its issue, repository policies, changed
behavior, and verification evidence. Treat `.github/pull_request_template.md`
as the source of truth; do not copy its checklist into this skill.

Prefer an available MCP tool for Git and GitHub operations. Use local Git or a
command-line client only when MCP is unavailable or does not support the
required operation.

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
4. Resolve the domain PR checklist set from the changed artifacts:
   - For each changed artifact, find its owning domain README and read every
     checklist that README explicitly identifies as a Pull Request review
     checklist.
   - Use the union of those checklists and evaluate a checklist once when
     multiple artifacts select it. When a changed domain has no registered PR
     checklist, apply only the common checklist to that domain and record that
     no domain PR checklist is registered.
   - For requirement artifacts, use
     `docs/design/requirement/software_requirement_review_checklist_pr.md` for
     every changed SWR and
     `docs/design/requirement/software_requirement_verification_spec_review_checklist_pr.md`
     for every changed SWRVS. Use both when both artifact types change.
   - For architecture artifacts, use
     `docs/design/architecture/architecture_design_review_checklist_pr.md` for
     every changed software architecture document and every changed ADR. Apply
     the checklist once when both artifact types change.
   - Never select a release-baseline or quality checklist during Pull Request
     review. In particular, exclude every `*_review_checklist_quality.md` file
     even when the Pull Request targets a release branch or establishes a
     release baseline. Quality evaluation belongs to a separate workflow.
   - Read the selected checklists in full and preserve their exact item text in
     the review summary.
5. Fetch check runs for the current head and use them as the CI source of truth.
   Start the review only when every check run is completed successfully. If any
   check is missing, pending, skipped, cancelled, or failed, stop and report the
   exact check state without posting a review. Do not treat an empty legacy
   combined-status result as pending when check runs contain the repository's
   CI results; report the API discrepancy instead.
6. Determine the review scope:
   - For an initial review, inspect the complete base-to-head change.
   - For a re-review, find the authenticated reviewer's latest valid submitted
     review commit and inspect changes from that commit through the current
     head. A valid prior review contains the template checklist with every row
     completed and exactly one decision; ignore casual or partial comments.
   - Treat this repository as a personal project. Do not require a separate
     reviewer or `CODEOWNERS`; the repository owner is the sole review owner for
     every area and performs self-review for self-authored Pull Requests.
   - On re-review, inspect only changes after the latest valid review commit.
     Retain review results for genuinely unaffected areas. Re-evaluate a retained
     trace or verification result when newly changed design, code, test, analysis,
     checklist, or configuration can invalidate it even if the linked SWR or
     SWRVS file did not change.
7. Classify every file in the complete reviewed change as direct implementation
   of the linked issue, necessary consequential policy or documentation, an
   eligible optional supporting tool, or unrelated work. Use only the linked
   GitHub Issue and repository policies as authoritative sources for scope,
   requirements, and acceptance criteria. A local plan may identify changed
   paths or provide non-authoritative context, but shall not add requirements or
   acceptance criteria. For each supporting tool, apply the eligibility,
   separate-issue, lifecycle, and repository or domain precedence rules in
   `docs/process/git_workflow.md`; confirm that every required disclosure
   appears in the Pull Request's `Supporting Tools` section; and include the
   tool in the normal quality review. Treat disclosed tool-internal schemas,
   references, metadata, scripts, state models, and validators as parts of the
   category 3 tool rather than as direct issue requirements when that policy
   makes the tool eligible. Do not fail `SCOPE` merely because such contracts
   apply during the tool's explicit opt-in operation. Fail `SCOPE` for unrelated
   work, an ineligible tool, missing disclosure, a repository-wide new norm or
   a prerequisite for issue acceptance or repository lifecycle verification,
   or a repository lifecycle bypass.
8. Classify the lifecycle gate before evaluating completeness:
   - `Requirement authoring`: for a new SWR, apply both the SWR and SWRVS PR
     checklists. Require all SWRVS artifacts needed to cover the SWR and complete
     bidirectional SWR-to-SWRVS trace in the same Pull Request. For an SWRVS-only
     correction, apply its checklist and confirm that the SWR obligation is
     unchanged. Permit an empty `Downstream` relationship and empty
     `Verification implementation` relationships while their targets do not
     exist. Do not require later lifecycle work in this Pull Request.
   - `Downstream implementation`: require the SWR, downstream design, and reverse
     trace updates in the same Pull Request. Do not require verification
     implementation unless the change claims verification readiness.
   - `Verification implementation`: require concrete implementation IDs and
     SWRVS links in the same Pull Request. Re-evaluate the affected VM and ACs.
   - `Verification-ready claim`: require complete bidirectional traceability,
     actual implementation links, and the PR evidence needed to support the
     claim. Do not apply release-baseline quality checklists.
9. Enforce the staged Pull Request boundary:
   - Require a new SWR and all SWRVS artifacts needed to cover it in the same
     requirement-authoring Pull Request.
   - Require a semantic SWR change and every affected AC or VM correction in the
     same authoring Pull Request. Permit an SWRVS-only correction when the SWR
     obligation does not change.
   - Permit verification implementation with trace-only updates to its accepted
     SWRVS.
   - Fail `SCOPE` when requirement authoring is combined with downstream design,
     product code, verification implementation, or results. Require a semantic
     authoring correction discovered during implementation to land first.
10. Trace requirements through implementation, tests, documentation, and build
   configuration. Prioritize correctness, safety, regressions, error paths,
   interface compatibility, ownership/lifetime, concurrency, and missing tests.
   Distinguish statement-level verifiability from lifecycle verification
   readiness. Do not report a permitted future relationship as missing, and do
   not require an unrelated Pull Request to repair pre-existing staged absence.
   Apply the Markdown link validation rules below to every changed Markdown link.
11. Reconcile existing threads before creating findings. Confirm whether each
   prior request is resolved in the current scope and avoid duplicating an
   active thread.
12. Complete every common checklist row from the PR template and every row from
    the resolved domain PR checklist set as `PASS`, `FAIL`, or justified `N/A`.
    Base each result on inspected evidence; do not infer that a test or check
    passed. Use the exact selected checklist text and group results by artifact.
13. Select exactly one decision using the template criteria:
   - `DO NOT MERGE` when any required item fails, evidence is missing, a CI
     check is not successful, or a blocking finding remains.
   - `MERGE` when all required items pass or have justified `N/A` results and no
     blocking finding remains.
   - `MERGE WITH FOLLOW-UP` only when acceptance criteria pass, findings are
     non-blocking, and each deferred finding links an existing follow-up issue.
   - Do not select `MERGE WITH FOLLOW-UP` merely because later lifecycle stages
     remain; staged absence allowed by the governing rule is not a finding.

## Markdown link validation

- Determine the Markdown rendering context before resolving a link.
- In a repository Markdown file, treat a link beginning with `/` as
  repository-root-relative. Strip the leading slash and validate the resulting
  path against the reviewed PR head.
- Resolve `./` and `../` links relative to the directory containing the source
   Markdown file.
- Validate fragments against headings and explicit anchors in the target file.
- Do not use a generic web URL resolver against a GitHub `blob` URL to determine
  how GitHub renders repository Markdown links.
- Report a broken-link finding only when the normalized repository target or
  fragment does not exist at the reviewed head, or the rendered GitHub target
  has been directly verified as invalid.
- Apply separate resolution rules to Markdown in issues, Pull Requests, and
  comments because their rendering context differs from repository files.

## Findings

Write only actionable findings caused by the PR. Attach each change request to
the narrowest relevant changed line. Use a file-level thread only when no single
line represents the problem.

Because the repository owner may act as both author and reviewer, prefix every
reviewer-authored review-thread comment, including findings and disputed-finding
outcomes, with `[Reviewer]` followed by one blank line. Do not add this marker
to the review-summary body.

Format each finding as:

```markdown
[Reviewer]

[BLOCKING] F-001: <concise problem>

<why this is a problem and the concrete failure mode>

Required change: <specific outcome required>
```

Use `NON-BLOCKING` only when the finding does not violate acceptance criteria,
create correctness or safety risk, or leave required verification incomplete.
Include the follow-up issue link in a deferred finding.

Do not modify the PR branch while acting as reviewer. Do not resolve an author's
thread until the current diff demonstrates that the requested outcome is met.

## Disputed findings

Follow the governing template's disputed-finding flow when the repository owner
disagrees with a finding during self-review:

1. Require the owner to reply in the original thread with rationale and
   objective evidence.
2. Evaluate the finding against the linked issue, project policies, and test or
   analysis evidence.
3. Record one outcome in the thread: retain the request, withdraw it, or change
   it to `NON-BLOCKING` with a linked follow-up issue.
4. Keep the thread unresolved and the decision as `DO NOT MERGE` while a
   blocking dispute remains.
5. If the finding remains disputed, require the repository owner to make the
   final decision and document why the evidence supports it in the same thread.
6. Resolve the thread only after its recorded outcome is reflected in the
   current change or the finding is withdrawn or validly deferred.

Require the repository owner to document the self-review evidence and final
decision for a self-authored Pull Request.

## GitHub submission

Write new narrative in local review drafts and temporary working files in the
language used by the user in the current request. Before posting review threads,
a review summary, or other formal remote content, explicitly ask the user to
confirm the target language and wait for both that choice and separate
authorization for submission. Use the confirmed language for new remote
narrative. A content-language change shall not translate or otherwise alter
this skill's Markdown headings, the Pull Request template's headings or fixed
wording, checklist identifiers, machine-readable tokens, commands, code, or
quoted source text.

Treat review submission as an external write. Inspect and draft the review when
the user asks only to review; post threads or submit a GitHub review only when
the user explicitly requests posting, submission, approval, or change requests.

For an authorized review with line findings:

1. Copy the review-summary block from `.github/pull_request_template.md`, fill
   every checklist result, select one decision, and replace every placeholder.
   Keep the decision, rationale, and follow-up issues visible. Put the complete
   common checklist and every checklist from the resolved domain PR checklist
   set inside the template's single `<details>` element. Put PASS, FAIL, and N/A
   totals in its summary and remove the domain placeholder section when no
   domain PR checklist is registered.
2. Store the complete review-summary body in one variable and do not rebuild it
   during submission. Count every PASS, FAIL, and N/A row from that body,
   validate its totals, and confirm that no placeholder remains before the
   first external write.
3. Create a pending review with `pull_request_review_write` method `create`,
   the current head SHA, and the finalized body. If the authenticated reviewer
   already has a pending review, reuse it only when its draft comments and head
   belong to the current transaction; otherwise delete it and create one
   pending review.
4. Add every finding with `add_comment_to_pending_review`. Use `RIGHT` for added
   or changed lines and `LEFT` for deleted lines.
5. Submit the pending review as `COMMENT` for a self-authored Pull Request,
   regardless of the selected decision, and pass the exact same finalized body
   variable to `submit_pending`. Do not replace it with a short status message;
   the submission body becomes the final review body. Do not attempt
   self-approval or self-requested changes. State that the completed checklist
   and selected decision are the required review record because GitHub prevents
   self-approval and self-requested changes.
6. Re-read the PR reviews and threads to verify that exactly one new submitted
   review has the finalized body, `COMMENTED` state, intended head SHA, and all
   intended line comments. Compare the complete body, not only the decision.
7. If the pending review needs correction before submission, update the local
   finalized body and pass it to `submit_pending`. If a draft line comment or
   reviewed head is wrong, delete the pending review and recreate the transaction.
8. If submission fails or post-submit verification finds a mismatch, stop
   without creating another submitted review. If the review is already
   immutable, report the mismatch and request explicit authorization before a
   corrective review.

For an authorized review without findings, a pending review is still preferred
so the same summary and verification sequence is used consistently.

## Output

Lead with the decision and lifecycle gate. List blocking findings before
non-blocking findings, include file and line references, summarize CI evidence,
and state whether the review was drafted or submitted. Keep detailed common and
domain checklist tables inside `<details>`. If submitted, link the PR and
identify the reviewed head SHA.
