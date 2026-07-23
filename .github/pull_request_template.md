## Summary

<!-- Briefly describe the purpose of this PR. -->

## Related Issue

close #

## Changes

<!-- List the key changes only. -->

-

## Verification

<!-- List executed commands/checks and their results or links. -->

-

## Review

<details>
<summary>Reviewer workflow, checklist, and review-summary template</summary>

Start review only after all CI checks pass.

This repository is maintained as a personal project. It does not require a
separate reviewer or `CODEOWNERS` assignment. The repository owner is the sole
review owner for every area and performs the self-review for self-authored Pull
Requests.

1. Add each change request to the relevant line as a review thread comment.
   Mark it `BLOCKING` or `NON-BLOCKING` and record its resolution or follow-up.
2. Submit a review summary using the checklist below and select `DO NOT MERGE`
   while any required item fails or a blocking finding remains.
3. After the author updates the PR, all CI checks pass, and review is requested
   again, the repository owner reviews only the newly changed areas and submits
   a new summary. Repeat until every required item passes and the owner records
   a final decision.

A new commit requires another review only for the areas changed by that commit;
review results for unaffected areas remain valid. Use `MERGE` when all required
items pass with no blocking findings. Use `MERGE WITH FOLLOW-UP` only when
acceptance criteria pass and each non-blocking finding links an issue.
Otherwise, use `DO NOT MERGE`.

### Disputed findings

If the author disagrees with a finding:

1. Reply in the same review thread with the rationale and objective evidence.
2. Evaluate the finding against the linked issue, project policies, and test or
   analysis evidence. The reviewer records whether the request is retained,
   withdrawn, or changed to `NON-BLOCKING` with a linked follow-up issue.
3. Keep the thread unresolved and the decision as `DO NOT MERGE` until the
   outcome is recorded and every blocking concern is resolved.
4. If a finding remains disputed after evaluation, the repository owner makes
   the final decision and documents why the evidence supports that decision in
   the same thread.
5. The reviewer resolves the thread only after the recorded outcome is applied
   to the current change or the finding is withdrawn or deferred.

GitHub does not permit the repository owner to approve a self-authored Pull
Request. Submit a `COMMENT` review for the current head containing the completed
checklist, objective evidence, and exactly one decision. This recorded decision
is the required review record; GitHub approval is not required.

Copy this block into the GitHub review summary. Record `PASS`, `FAIL`, or `N/A`
for every item and explain every `N/A`.

```markdown
### Checklist

| ID | Result | Review check and evidence or N/A reason |
| --- | --- | --- |
| SCOPE | PASS / FAIL / N/A | Matches the issue; no unrelated work. |
| TRACE | PASS / FAIL / N/A | Requirements, design, code, tests, and docs are consistent. |
| CORRECT | PASS / FAIL / N/A | Normal, boundary, error, state, and concurrency behavior is correct. |
| INTERFACE | PASS / FAIL / N/A | Compatibility, ownership, lifetime, errors, and thread safety are explicit. |
| MAINTAIN | PASS / FAIL / N/A | Follows guidelines without avoidable duplication or complexity. |
| VERIFY | PASS / FAIL / N/A | Verification covers changed behavior and regression risk. |
| EVIDENCE | PASS / FAIL / N/A | Applicable build, test, format, analysis, and CI results pass. |
| DOC | PASS / FAIL / N/A | Applicable user, API, configuration, and process docs are updated. |
| FINDINGS | PASS / FAIL / N/A | No blocking finding remains; deferred findings link follow-up issues. |

### Decision

- [ ] MERGE
- [ ] DO NOT MERGE
- [ ] MERGE WITH FOLLOW-UP

Rationale: <why the current change is or is not acceptable>

Follow-up issues: <issue links, or None>
```

</details>
