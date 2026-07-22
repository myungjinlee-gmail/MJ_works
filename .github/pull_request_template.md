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

1. Add each change request to the relevant line as a review thread comment.
   Mark it `BLOCKING` or `NON-BLOCKING` and record its resolution or follow-up.
2. Submit a review summary using the checklist below and select `DO NOT MERGE`
   while any required item fails or a blocking finding remains.
3. After the author updates the PR, all CI checks pass, and review is requested
   again, only the owners of the changed areas review the new changes and
   submit new summaries. Repeat until every required item passes and every
   required owner approves.

A new commit requires another review only from the owners of the areas changed
by that commit; approvals for unaffected areas remain valid. Use `MERGE` when
all required items pass with no blocking findings. Use `MERGE WITH FOLLOW-UP`
only when acceptance criteria pass and each non-blocking finding links an
issue. Otherwise, use `DO NOT MERGE`.

Submit GitHub approval only with the final `MERGE` or
`MERGE WITH FOLLOW-UP` summary for the current head.

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
