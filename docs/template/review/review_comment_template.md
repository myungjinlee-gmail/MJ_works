# Review Comment Template

Copy the content below into a Pull Request conversation comment immediately
before merge.

```markdown
## Self Review

- PR: #<pull-request-number>
- Related issue: #<issue-number>
- Reviewed head SHA: `<full-commit-sha>`
- Reviewed at: <YYYY-MM-DD HH:MM timezone>

### Checklist

| ID | Result | Evidence or N/A reason |
| --- | --- | --- |
| SCOPE | PASS / FAIL / N/A | |
| TRACE | PASS / FAIL / N/A | |
| CORRECT | PASS / FAIL / N/A | |
| INTERFACE | PASS / FAIL / N/A | |
| MAINTAIN | PASS / FAIL / N/A | |
| VERIFY | PASS / FAIL / N/A | |
| EVIDENCE | PASS / FAIL / N/A | |
| DOC | PASS / FAIL / N/A | |
| FINDINGS | PASS / FAIL / N/A | |

### Findings

| ID | Classification | Status | Resolution or follow-up issue |
| --- | --- | --- | --- |
| None | - | - | - |

### Decision

- [ ] MERGE
- [ ] DO NOT MERGE
- [ ] MERGE WITH FOLLOW-UP

Rationale: <why the current change is or is not acceptable>

Follow-up issues: <issue links, or None>

This decision applies only to the reviewed head SHA. A new commit invalidates
the decision and requires a new self-review comment.
```
