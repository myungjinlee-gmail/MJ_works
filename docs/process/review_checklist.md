# Review Checklist

Use this checklist with the
[review comment template](../template/review/review_comment_template.md).
Record each item as `PASS`, `FAIL`, or `N/A`; every `N/A` requires a reason.

| ID | Required check |
| --- | --- |
| `SCOPE` | The change matches the linked issue and contains no unrelated work. |
| `TRACE` | Affected requirements, design, source, tests, and documentation are consistent and linked, or non-applicability is explained. |
| `CORRECT` | Normal, boundary, error, state, and applicable concurrency behavior are correct. |
| `INTERFACE` | Compatibility, ownership, lifetime, error behavior, and thread safety of affected interfaces are explicit. |
| `MAINTAIN` | The change follows the coding guideline and introduces no avoidable duplication, dead code, or unnecessary complexity. |
| `VERIFY` | Verification has defined pass/fail criteria and covers changed behavior and regression risk. |
| `EVIDENCE` | Applicable build, test, format, static-analysis, and CI results are recorded and passing. |
| `DOC` | User, API, configuration, and process documentation are updated, or non-applicability is explained. |
| `FINDINGS` | No blocking finding remains; each deferred non-blocking finding links a follow-up issue. |

These checks use the Automotive SPICE 4.0 principles of consistency,
traceability, defined verification criteria, recorded results, and communicated
evidence. They are project review criteria, not an Automotive SPICE or
ISO 26262 compliance claim.
